import os

# 友達追加時メッセージ
def follow_event_message():
    return """【横浜市ゴミ分別検索システム】
<利用方法>
・ 分別方法を知りたいものの写真を送信するか、名称をチャットで送信してください。
・ 分別方法や廃棄時の注意事項を返信でお知らせします。
<注意事項>
・個人情報を特定できるような写真は送信しないでください。
・正しい検索結果を得られない場合があります。その際には、別の角度から撮った画像を送信するか、別の名称をチャットで送信してください。"""

# 「使い方」というテキストを受信した時のメッセージ
def usage_message():
    return """【横浜市ゴミ分別検索システム】
<利用方法>
・ 分別方法を知りたいものの写真を送信するか、名称をチャットで送信してください。
・ 分別方法や廃棄時の注意事項を返信でお知らせします。
<注意事項>
・個人情報を特定できるような写真は送信しないでください。
・正しい検索結果を得られない場合があります。その際には、別の角度から撮った画像を送信するか、別の名称をチャットで送信してください。"""

# テキスト検索 リスト該当なし時のメッセージ
def text_noresult_message():
    return """【検索結果: 該当なし】
該当するものが見つかりませんでした。
別の名称や言い回しを変えてもう一度送信してください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""

# 画像検索 認識失敗時のメッセージ
def image_not_recognized_message():
    return """【認識失敗】
写真から物体を認識できませんでした。
別の角度から撮った画像を送信するか、名称をテキストで送信してください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""

# 画像検索 認識できたがリスト該当なし時のメッセージ
def image_recognized_noresult_message(object_list):
    message = "【認識結果】\n"
    for obj in object_list:
        message += f"・{obj}\n"
    message += """該当するものが見つかりませんでした。
正しい認識結果でしたか？
正しい認識結果でなかった場合は、別の角度から撮った画像を送信するか、名称をテキストで送信してください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
    return message

# テキスト検索・画像検索共通 リスト該当あり時のカルーセルメッセージ
def search_carousel_template(search_result):
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

    carousel_columns = []
    for i, result in enumerate(search_result):
        # カルーセルの最大表示数は10件のみ
        if i == 10:
            break

        carousel_title = result["name"]
        if len(carousel_title) >= 40:
            carousel_title = carousel_title[:39] + "…"

        carousel_text = f"【{result['category']}】"
        if len(result["info"]) > 0:
            carousel_text += f"\n{result['info']}"
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
                        label="詳細を見る",
                        uri=carousel_url
                    )
                ]
            )
        )
    return CarouselTemplate(columns=carousel_columns)

# 画像検索 リスト該当あり時の補足メッセージ
# 結果をカルーセルで返した後に送信する
# 画像認識結果(英)と誤認識用のフォローアップメッセージ
def image_recognized_supplementary_message(object_list):
    message = "【認識結果】\n"
    for obj in object_list:
        message += f"・{obj}\n"
    message += """正しい認識結果でしたか？
正しい認識結果でなかった場合は、別の角度から撮った画像を送信するか、名称をテキストで送信してください。
また、横浜市ごみと資源物の出し方一覧表も合わせてご覧ください。
https://cgi.city.yokohama.lg.jp/shigen/bunbetsu/list.html"""
    return message

