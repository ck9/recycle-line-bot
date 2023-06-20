import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.linebot as line_bot

def main():
    userid_dummy = "f947tgun443ddqvfjcwt2bpt6kt5aqva"

    print("--インスタンス生成--")
    # ダミーのユーザーIDを設定
    LineBot = line_bot.LineBot(userid_dummy)
    print("get_user_lang()出力: "+LineBot.get_user_lang())
    print("--言語設定を英語に変更--")
    print("set_user_lang('en')出力: "+LineBot.set_user_lang("en"))
    print("get_user_lang()出力: "+LineBot.get_user_lang())
    print("--言語設定を日本語に変更--")
    print("set_user_lang('ja')出力: "+LineBot.set_user_lang("ja"))
    print("get_user_lang()出力: "+LineBot.get_user_lang())
    print("--言語設定を切り替え--")
    print("change_user_lang()出力: "+LineBot.change_user_lang())
    print("get_user_lang()出力: "+LineBot.get_user_lang())

    return

if __name__ == '__main__':
    main()