import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import src.search as search

def main():

    print("--インスタンス生成--")
    Search = search.Search()
    print("--日本語検索--")
    print("search_ja('トイレットペーパーの芯')出力: "+str(Search.search_ja("トイレットペーパーの芯")))
    print("--英語検索--")
    print("search_en(['toilet paper core'])出力: "+str(Search.search_en(["toilet paper core"])))

    return

if __name__ == '__main__':
    main()