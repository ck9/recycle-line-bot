import os
from flask import Flask, request, abort, render_template
from dotenv import load_dotenv

this_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(this_dir, '.env'))

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, ImageMessage, TextSendMessage, TemplateSendMessage,  CarouselTemplate, CarouselColumn, URITemplateAction
)
import os

from src.search import search_ja, search_en
import src.image_recognition as img_recognition
import src.linebot as line_bot

app = Flask(__name__, static_url_path='/static')

line_access_token = os.environ.get("LINE_ACCESS_TOKEN")
line_channel_secret = os.environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(line_access_token)
handler = WebhookHandler(line_channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 友達追加時のイベント
@handler.add(FollowEvent)
def follow_message(event):
    if event.type == "follow":
        user_id = event.source.user_id
        LineBot = line_bot.LineBot(user_id)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=LineBot.follow_message()))
    return

# テキスト受信時のイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    LineBot = line_bot.LineBot(user_id)
    # 「使い方」というメッセージを受信した場合
    if event.message.text in ["使い方", "usage", "ヘルプ", "help"]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=LineBot.usage_message()))
        return
    # 「japanese」というメッセージを受信した場合(言語設定変更)
    elif event.message.text in ["ja", "japanese", "日本語"]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=LineBot.set_user_lang(user_id, "ja")))
        return
    # 「英語」というメッセージを受信した場合
    elif event.message.text in ["en", "english", "英語"]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=LineBot.set_user_lang(user_id, "en")))
    # それ以外のメッセージを受信した場合(テキスト名称検索)
    else:
        if LineBot.get_user_lang() == "ja":
            result = search_ja(event.message.text)
        else:
            result = search_en([event.message.text])
        # リスト検索結果が0件の場合
        if len(result) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=LineBot.text_noresult_message()))
            return
        # リスト検索結果が存在する場合(カルーセル表示)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(alt_text='検索結果', template=LineBot.search_carousel_template(result)))
            return
    
# 画像受信時のイベント
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    user_id = event.source.user_id
    LineBot = line_bot.LineBot(user_id)

    # 画像のバイナリデータを取得して保存
    message_content = line_bot_api.get_message_content(message_id)
    img_dir = os.path.join(this_dir, "static", "tmp")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    with open(os.path.join(img_dir, f"{message_id}.jpg"), "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    vision_ai = img_recognition.VisionAI()
    # 画像認識
    object_list = vision_ai.recognize_path(os.path.join(img_dir, f"{message_id}.jpg"))
    # object_list = image_vision("https://recycle-bot.ck9.jp/static/tmp/" + f"{message_id}.jpg")
    
    # 画像をすぐに削除
    # os.remove(os.path.join(img_dir, f"{message_id}.jpg"))

    # 画像認識に失敗した場合
    if len(object_list) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=LineBot.image_not_recognized_message()))
        return
    # 画像認識に成功した場合
    else:
        result = search_en(object_list)
        # リスト検索結果が0件の場合
        if len(result) == 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=LineBot.image_recognized_noresult_message(object_list)))
            return
        # リスト検索結果が存在する場合(カルーセル表示+補足メッセージ)
        else:
            line_bot_api.reply_message(
                event.reply_token,[
                    TemplateSendMessage(alt_text='検索結果', template=LineBot.search_carousel_template(result)),
                    TextSendMessage(text=LineBot.image_recognized_supplementary_message(object_list))
                ])
            return
        

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run()
