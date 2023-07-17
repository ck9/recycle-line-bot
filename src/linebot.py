import os, json

this_dir = os.path.dirname(os.path.abspath(__file__))

class LineBot:

    user_json_path = os.path.join(this_dir, 'user_info.json')
    user_obj_json_path = os.path.join(this_dir, 'user_last_object.json')

    def __init__(self, user_id):
        
        # json読み込み (存在しない場合は作成)
        user_lang_dict = {}
        if not os.path.exists(self.user_json_path):
            with open(self.user_json_path, 'w') as f:
                json.dump(user_lang_dict, f)
        else:
            with open(self.user_json_path, 'r') as f:
                user_lang_dict = json.load(f)

        user_obj_dict = {}
        if not os.path.exists(self.user_obj_json_path):
            with open(self.user_obj_json_path, 'w') as f:
                json.dump(user_obj_dict, f)
        else:
            with open(self.user_obj_json_path, 'r') as f:
                user_obj_dict = json.load(f)
        
        # ユーザーIDが存在しない場合は追加しjsonを更新
        if user_id not in user_lang_dict:
            user_lang_dict[user_id] = "ja"
            with open(self.user_json_path, 'w') as f:
                json.dump(user_lang_dict, f)
        if user_id not in user_obj_dict:
            user_obj_dict[user_id] = ["nohistory"]
            with open(self.user_obj_json_path, 'w') as f:
                json.dump(user_obj_dict, f)

        # ユーザーIDに対応する言語を取得しuser_langに格納
        self.user_lang = user_lang_dict[user_id]
        self.user_id = user_id

        self.user_obj = user_obj_dict[user_id]

    # ユーザーの言語設定を変更 (lang: "ja" or "en")
    def set_user_lang(self, lang):
        if lang not in ["ja", "en"]:
            return
        with open(self.user_json_path, 'r') as f:
            user_lang_dict = json.load(f)
        user_lang_dict[self.user_id] = lang
        with open(self.user_json_path, 'w') as f:
            json.dump(user_lang_dict, f)
        self.user_lang = lang
        message_ja = "言語設定を日本語に変更しました。"
        message_en = "Changed the language setting to English."
        return message_ja if self.user_lang == "ja" else message_en
    
    def change_user_lang(self):
        if self.user_lang == "ja":
            return self.set_user_lang("en")
        else:
            return self.set_user_lang("ja")
        
    def set_user_last_object(self, last_object):
        with open(self.user_obj_json_path, 'r') as f:
            user_obj_dict = json.load(f)
        user_obj_dict[self.user_id] = last_object
        with open(self.user_obj_json_path, 'w') as f:
            json.dump(user_obj_dict, f)
        self.user_obj = last_object
        return
    
    def get_user_lang(self):
        return self.user_lang
    
    def get_user_last_object(self):
        return self.user_obj
    
    # 友達追加時メッセージ
    def follow_event_message(self):
        message_ja = """【横浜市ゴミ分別検索システム】
<利用方法>
・ 分別方法を知りたいものの写真を送信するか、名称をチャットで送信してください。
・ 分別方法や廃棄時の注意事項を返信でお知らせします。
・If you want to search in English, please send "English" or “英語”.
<注意事項>
・個人情報を特定できるような写真は送信しないでください。
・正しい検索結果を得られない場合があります。その際には、別の角度から撮った写真を送信するか、別の名称をチャットで送信してください。
・写真の背景に物が映らないようにしてください。
・プライバシーポリシーはこちらをご覧ください。
https://recycle-bot.ck9.jp/privacy 
"""
        message_en = """Yokohama City Garbage Separation Search System
<How to use>
・Please send us a photo of the item you want to know how to sort, or send us the name of the item via chat.
・We will send you a reply with instructions on how to sort and what to do when disposing of the items.
・日本語で検索したい場合は「日本語」または「Japanese」と送信してください。
<Cautions>
・Please do not send photos that can identify your personal information.
・Please do not send photos that may identify personal information. In such cases, please send a picture taken from a different angle or send a different name in the chat.
・Please make sure that no objects appear in the background of the photo.
・Please click here to view our privacy policy.
https://recycle-bot.ck9.jp/privacy 
"""
        return message_ja if self.user_lang == "ja" else message_en

    # 「使い方」というテキストを受信した時のメッセージ
    def usage_message(self):
        # 友だち追加時のメッセージと共通化
        return self.follow_event_message()
    
    # 「「画像で検索」というテキストを受信した時のメッセージ
    def search_by_picture_message(self):
        message_ja = """【画像で検索】
分別方法を知りたいものの写真を送信してください。
分別方法や廃棄時の注意事項を返信でお知らせします。
画像の背景に物が映らないよう、正面から撮影してください。"""
        message_en = """【Search by picture】
Please send us a photo of the item(s) you want to know how to sort.
We will send you a reply with the sorting method and precautions for disposal.
Please take a picture from the front so that the object does not appear in the background of the picture."""
        return message_ja if self.user_lang == "ja" else message_en

    # 「テキストで検索」というテキストを受信した時のメッセージ
    def search_by_text_message(self):
        message_ja = """【テキストで検索】
分別方法を知りたいものの名称をチャットで送信してください。
分別方法や廃棄時の注意事項を返信でお知らせします。"""
        message_en = """【Search by text】
Send us a chat with the name of the item you want to know how to sort.
We will send you a reply with the sorting method and precautions for disposal."""
        return message_ja if self.user_lang == "ja" else message_en
        
    # テキスト検索 リスト該当なし時のメッセージ
    def text_noresult_message(self):
        message_ja =  """【検索結果: 該当なし】
該当するものが見つかりませんでした。
別の名称や言い回しを変えてもう一度送信してください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
        message_en = """【Search result: Not found】
No matches found.
Please change another name or wording and submit again.
Please also see the list of how to dispose of Yokohama City garbage and resources.
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
        return message_ja if self.user_lang == "ja" else message_en

    # 画像検索 認識失敗時のメッセージ
    def image_not_recognized_message(self):
        message_ja =  """【認識失敗】
写真から物体を認識できませんでした。
別の角度から撮った写真を送信するか、名称をテキストで送信してください。
写真の背景に物が映らないようにしてください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html
"""
        message_en = """【Image Recognition failed】
The object could not be recognized from the photo.
Please send an image taken from a different angle or send the name as text.
Please make sure that no objects appear in the background of the photo.
Please also see the list of how to dispose of garbage and recyclables in Yokohama City.
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
        return message_ja if self.user_lang == "ja" else message_en

    # 画像検索 認識できたがリスト該当なし時のメッセージ
    def image_recognized_noresult_message(self, object_list):
        message = "【認識結果】\n" if self.user_lang == "ja" else "【Recognition result】\n"
        for obj in object_list:
            message += f"・{obj}\n"
        message_ja = """該当するものが見つかりませんでした。
正しい認識結果でしたか？
正しい認識結果でなかった場合は、別の角度から撮った画像を送信するか、名称をテキストで送信してください。
写真の背景に物が映らないようにしてください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
        message_en = """No match found.
If it was not a correct recognition result, please send us an image taken from a different angle or send us the name in text.
Please make sure that no objects appear in the background of the photo.
Also, please refer to the list of how to dispose of garbage and recyclables in Yokohama City.
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html
"""
        message += message_ja if self.user_lang == "ja" else message_en
        return message

    # テキスト検索・画像検索共通 リスト該当あり時のカルーセルメッセージ
    def search_carousel_template(self, search_result):
        from linebot.models import CarouselTemplate, CarouselColumn, URITemplateAction
        yokohama_urls = {
            "燃やすごみ": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das1.html",
            "燃えないごみ": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das11.html",
            "乾電池": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das4.html",
            "スプレー缶": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das10.html",
            "缶・びん・ペットボトル": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das2.html",
            "小さな金属類": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das8.html",
            "プラスチック製容器包装": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/das12.html",
            "粗大ごみ": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/shushu/sodaigomi/",
            "Other": "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/gomi-recycle/gomi/"
        }

        carousel_templates = []
        carousel_columns = []
        for i, result in enumerate(search_result):
            # カルーセルの最大表示数は10件のみ
            if i % 10 == 9:
                carousel_templates.append(CarouselTemplate(columns=carousel_columns))
                carousel_columns = []
                if i == 29:
                    break

            if self.user_lang == "ja":
                # カルーセルタイトル (日本語)
                carousel_title = result["name"]
                if len(carousel_title) >= 40:
                    carousel_title = carousel_title[:39] + "…"
                # カルーセルテキスト (日本語)
                carousel_text = f"【{result['category']}】"
                if len(result["info"]) > 0:
                    carousel_text += f"\n{result['info']}"
                if len(carousel_text) >= 60:
                    carousel_text = carousel_text[:59] + "…"
            else:
                # カルーセルタイトル (英語)
                carousel_title = result["name_en"]
                if len(carousel_title) >= 40:
                    carousel_title = carousel_title[:39] + "…"
                # カルーセルテキスト (英語)
                carousel_text = f"【{result['category_en']}】"
                if len(result["info_en"]) > 0:
                    carousel_text += f"\n{result['info_en']}"
                if len(carousel_text) >= 60:
                    carousel_text = carousel_text[:59] + "…"

            if result["category"] in yokohama_urls:
                carousel_url = yokohama_urls[result["category"]]
            else:
                carousel_url = yokohama_urls["Other"]

            carousel_columns.append(
                CarouselColumn(
                    title=carousel_title,
                    text=carousel_text,
                    actions=[
                        URITemplateAction(
                            label="詳細を見る" if self.user_lang == "ja" else "More info",
                            uri=carousel_url
                        )
                    ]
                )
            )
        if len(carousel_columns) > 0:
            carousel_templates.append(CarouselTemplate(columns=carousel_columns))
        return carousel_templates

    # 画像検索 リスト該当あり時の補足メッセージ
    # 結果をカルーセルで返した後に送信する
    # 画像認識結果(英)と誤認識用のフォローアップメッセージ
    def image_recognized_supplementary_message(self, object_list):
        message = "【認識結果】\n" if self.user_lang == "ja" else "【Recognition result】\n"
        for obj in object_list:
            message += f"・{obj}\n"
        message_ja = """正しい認識結果でしたか？
正しい認識結果でなかった場合は、別の角度から撮った画像を送信するか、名称をテキストで送信してください。
写真の背景に物が映らないようにしてください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
        message_en = """Was the recognition result correct?
If it was not a correct recognition result, please send us an image taken from a different angle or send us the name in text.
Please make sure that no objects appear in the background of the photo.
Also, please refer to the list of how to dispose of garbage and recyclables in Yokohama City.
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html
"""
        message += message_ja if self.user_lang == "ja" else message_en
        return message

    def image_recognized_supplementary_button_template(self):
        from linebot.models import CarouselTemplate, CarouselColumn, URITemplateAction, MessageTemplateAction
        return CarouselTemplate(
            columns=[
                CarouselColumn(
                    text="正しい認識結果でしたか？\n他の候補を表示できます" if self.user_lang == "ja" else "Did you get the right recognition result? There are other search results",
                    actions=[
                        MessageTemplateAction(
                            type="message",
                            label="他の候補を表示する👀" if self.user_lang == "ja" else "Show other results👀",
                            text="Other results"
                        )
                    ]
                )
            ]
        )