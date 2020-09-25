'''
= レースデータを取得 =
・レースID(csv)を"race_id"フォルダに用意してね
・欠損値には0を入れる

出力形式(json)
[
  {
    "netkeiba_id":"202002020103",
    "レース名":"3歳未勝利",
    "馬場状態": "芝",
    "周り方":"右",
    "距離": 1200,
    "天気": "晴",
    "開催日":"2020年07月04日",
    "賞金":[5100000,2000000,1300000,770000,510000],
    "競走馬": [
      {
        "競走馬ID":"2017102809",
        "順位": 1,
        "馬番": 2,
        "性別": "牡",
        "年齢": 2,
        "斤量": 54.0
        "単勝オッズ": 4.7,
        "体重": 512,
        "体重増減": 8
      },
      {
          ...(その他の競走馬データ)...
      }
    ]
  },
  {
      ...(その他のレースデータ)...
  }
]
'''


import csv
import race
from pprint import pprint
import json


def main():
    base_url = 'https://db.netkeiba.com/race/'
    id_list = []  # ['202002020103']
    year = '2021'

    # レースIDの読み込み
    with open('race_id/race_id'+year+'.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            id_list = row
        print(id_list)

    # レースデータ取得
    race_data = race.get_race_data(base_url, id_list)
    # pprint(race_data, width=80)

    # json形式に変換し保存
    with open('race_data/race_data_'+year+'.json', 'w') as f:
        json.dump(race_data, f, ensure_ascii=False,
                  indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
