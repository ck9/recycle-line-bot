import os, sys
import pandas as pd

this_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(this_dir, 'list.csv')
df = pd.read_csv(csv_path, encoding='utf-8', index_col=0)

class Search:

    def gen_response(self, search_results):
        response = []
        id_list = []
        for search_result in search_results:
            for i, row in search_result.iterrows():
                if i not in id_list:
                    id_list.append(i)
                    response.append({
                        "name": row["品目名_output"],
                        "category": row["出し方"],
                        "info": row["出し方のポイント"] if str(row["出し方のポイント"]) != "nan" else "",
                        "name_en": row["item_name_output"],
                        "category_en": row["category"],
                        "info_en": row["point"] if str(row["point"]) != "nan" else "",
                    })
        return response

    # 日本語テキスト検索(引数:品目名(String), 戻り値:検索結果(List))
    def search_ja(self, object_name):
        search_result = df[df['品目名'].str.contains(object_name, na=False)]
        return self.gen_response([search_result])

    # 英語完全一致検索(引数:品目名リスト(List), 戻り値:検索結果(List))
    def search_en_perfect(self, object_list):
        for i, object_name in enumerate(object_list):
            object_list[i] = object_name.lower()
        search_results = []
        # 完全一致で検索
        search_column = ["完全一致1", "完全一致2", "完全一致3"]
        for cname in search_column:
            search_result = df[df[cname].isin(object_list)]
            search_results.append(search_result)
        return self.gen_response(search_results)

    # 英語部分一致検索(引数:品目名リスト(List), 戻り値:検索結果(List))
    def search_en(self, object_list):
        for i, object_name in enumerate(object_list):
            object_list[i] = object_name.lower()
        search_results = []
        for object_name in object_list:
            search_result = df[df['item_name'].str.contains(object_name, na=False)]
            search_results.append(search_result)
        return self.gen_response(search_results)
    
    def import_list(self):
        df = pd.read_csv(csv_path, encoding='utf-8', index_col=0)
        df = df[df['頭文字'].notnull()]
        for i in df.index:
            df.at[i, "item_name"] = str(df.at[i, "item_name"]).lower()
            df.at[i, "完全一致1"] = str(df.at[i, "完全一致1"]).lower()
            df.at[i, "完全一致2"] = str(df.at[i, "完全一致2"]).lower()
            df.at[i, "完全一致3"] = str(df.at[i, "完全一致3"]).lower()
        df.to_csv(csv_path, encoding='utf-8')

def main():
    s = Search()
    s.import_list()
    name = input("name:")
    if len(sys.argv) > 1 and sys.argv[1] == "en":
        print("完全一致検索")
        print(s.search_en_perfect([name]))
        print("部分一致検索")
        print(s.search_en([name]))
    else:
        print(s.search_ja(name))

if __name__ == '__main__':
    main()