import os, json
import pandas as pd

this_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(this_dir, 'list.csv')
df = pd.read_csv(csv_path, encoding='utf-8', index_col=0)

def search_ja(name):
    search_result = df[df['品目名'].str.contains(name, na=False)]
    response = []
    for i, row in search_result.iterrows():
        response.append({
            "name": row["品目名"],
            "category": row["出し方"],
            "info": row["出し方のポイント"],
        })
    response = json.dumps(response, ensure_ascii=False, indent=2)
    return response

def main():
    name = input("name:")
    print(search_ja(name))

if __name__ == '__main__':
    main()