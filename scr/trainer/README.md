# 調教師マスタ収集

## 準備

trainer_id ディレクトリに trainer_id.csv が存在しない場合には，
次を実行して調教師 ID を取得してください．

```sh
cd trainer_id
python main.py
```

## 実行

```sh
cd trainer_record
python main.py
```

取得に成功すると，"trainer_master.json"が生成されます．

## 出力形式

- 取得対象：全調教師（所属\[美浦、栗東、地方、海外\]）
- 近走成績が 0 件の騎手の勝率と平均順位には 0 埋め
- 順位が数値でないものは除外
  (''(なし),'除','中','取','失','降','再')

## データ構造

```
[
    {
        "netkeiba_id":"5桁の調教師id(文字列型)",
        "name":"調教師名",
        "win_rate":直近20件の勝率(小数),
        "rank_average":直近20件の平均順位(小数)
    },
    {...},
    {...},
    ...
]
```
