'''
= レースデータを取得 =
・レースIDのCSVファイルを用意してね
・欠損値には０を入れる
'''
'''
出力形式
{
  "racedata": [
    {
      "馬場状態": "芝",
      "距離": 1200,
      "天気": "晴",
      "競走馬": [
        {
          "枠": 2,
          "性別": "牡",
          "年齢": 2,
          "順位": 1,
          "単勝オッズ": 4.7,
          "体重": 512,
          "体重増減": -10,
          "斤量": 54.0
        },
        {
            ...
        }
      ]
    },
    {
        ...
    }
  ]
}
'''




import csv
import race
from pprint import pprint
import json
def main():
    base_url = 'https://db.netkeiba.com/race/'
    race_ids = []  # [202002020103]
    year = '20'

    # レースIDの読み込み
    with open('race_id/race_id'+year+'.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            race_ids = row
        print(race_ids)

    # レースデータ取得
    race_data = race.get_race_data(base_url, race_ids)
    # pprint(race_data, width=80)

    # json形式に変換し保存
    with open('race_data/race_data_'+year+'.json', 'w') as f:
        json.dump(race_data, f, ensure_ascii=False,
                  indent=2, sort_keys=True, separators=(',', ': '))

        json.dump(race_data, f, ensure_ascii=False)


if __name__ == '__main__':
    main()

    # SITE_URL = []
    # for race in race_id_2020.race_id:
    #     SITE_URL.append("https://race.netkeiba.com"+race)
    # print(SITE_URL)
