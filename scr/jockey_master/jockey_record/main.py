'''
騎手マスタを取得
・取得対象：現役、引退騎手
・近走成績が0件の騎手の勝率と平均順位には0埋め
・順位が数値でないものは除外
    (''(なし),'除','中','取','失','降','再')

出力形式
[
    {
        "netkeiba_id":"５桁の騎手id",
        "name":"騎手名",
        "win_rate":"直近20件の勝率",
        "rank_average":"直近20件の平均順位"
    },
    {...},
    {...},
    ...
]
'''


from pprint import pprint
import json
import csv
import scp
import jockey


def main():
    base_url = 'https://db.netkeiba.com/jockey/'

    # id_list = ['05339', 'z0327', 'a005b', 'a015a']    #テスト用
    # csvファイルを開いて騎手IDを取得
    with open("../jockey_id/jockey_id.csv") as f:
        for row in csv.reader(f):
            id_list = row
        print(id_list)

    # すべての騎手id、騎手名を取得
    jockey_data = jockey.get_all_jockey_data(id_list, base_url)
    # pprint(jockey_data)

    # json形式に変換し保存
    with open('jockey_master.json', 'w') as f:
        json.dump(jockey_data, f, ensure_ascii=False,
                  indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
