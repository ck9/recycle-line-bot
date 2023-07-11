import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.image_recognition as img_rec

def main():

    print("--インスタンス生成--")
    VisionAI = img_rec.VisionAI()
    print("--画像URLからオブジェクト検出--")
    img_url = "https://m.media-amazon.com/images/I/61T9-ew0FdL._AC_UX679_.jpg"
    print("recognize_url(img_url)出力: "+str(VisionAI.recognize_url(img_url)))

    return

if __name__ == '__main__':
    main()