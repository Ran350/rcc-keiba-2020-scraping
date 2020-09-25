'''
調教師マスタを取得
・近走成績が0件の調教師の勝率と平均順位には0埋め
・順位が数値でないものは除外
    (''(なし),'除','中','取','失','降','再')

出力形式
[
    {
        "netkeiba_id":"５桁の調教師id",
        "name":"調教師名",
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
import trainer


def main():
    base_url = 'https://db.netkeiba.com/trainer/'

    # id_list = ['01163']
    # csvファイルを開いて騎手IDを取得
    with open("../trainer_id/trainer_id.csv") as f:
        for row in csv.reader(f):
            id_list = row
        print(id_list)

    # すべての騎手id、騎手名を取得
    trainer_data = trainer.get_all_trainer_data(id_list, base_url)
    # pprint(trainer_data)

    # json形式に変換し保存
    with open('trainer_master.json', 'w') as f:
        json.dump(trainer_data, f, ensure_ascii=False,
                  indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
