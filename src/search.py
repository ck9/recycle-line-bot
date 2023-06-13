import os, sys
import pandas as pd

this_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(this_dir, 'list.csv')
df = pd.read_csv(csv_path, encoding='utf-8', index_col=0)

# 日本語テキスト検索(引数:品目名(String), 戻り値:検索結果(List))
def search_ja(object_name):
    search_result = df[df['品目名'].str.contains(object_name, na=False)]
    response = []
    for i, row in search_result.iterrows():
        response.append({
            "name": row["品目名"],
            "category": row["出し方"],
            "info": row["出し方のポイント"] if str(row["出し方のポイント"]) != "nan" else "",
        })
    return response

# 英語テキスト検索(引数:品目名リスト(List), 戻り値:検索結果(List))
def search_en(object_list):
    response = []
    for object_name in object_list:
        search_result = df[df['Item name'].str.contains(object_name, na=False)]
        for i, row in search_result.iterrows():
            response.append({
                "name": row["品目名"],
                "category": row["出し方"],
                "info": row["出し方のポイント"] if str(row["出し方のポイント"]) != "nan" else "",
            })

    return response

def main():
    name = input("name:")
    if len(sys.argv) > 1 and sys.argv[1] == "en":
        print(search_en([name]))
    else:
        print(search_ja(name))

if __name__ == '__main__':
    main()