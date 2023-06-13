import os
from flask import Flask, request, abort
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
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

# import logging
# LOGFILE_NAME = "DEBUG.log"
# app.logger.setLevel(logging.DEBUG)
# log_handler = logging.FileHandler(LOGFILE_NAME)
# log_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(log_handler)

line_access_token = os.environ.get("LINE_ACCESS_TOKEN")
line_channel_secret = os.environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(line_access_token)
handler = WebhookHandler(line_channel_secret)

@app.route("/recycle-linebot", methods=['POST'])
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
