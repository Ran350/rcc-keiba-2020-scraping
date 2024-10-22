# 競走馬マスタ収集

## 準備

horse_id/horse_id/ ディレクトリ に horse_id1.csv が存在しない場合には，次を実行して競走馬 ID を取得してください．

```sh
python horse_id/main.py
```

実行が完了すると，scr/horse/horse_id/horse_id/ ディレクトリに horse_id.csv が生成されます．
各 horse_id.csv には，獲得賞金が多い競走馬順に，5000 件の競走馬 ID が 1 行で記述されます．

## 実行

```sh
python src/horse/src/main.py
```

取得に成功すると，horse_master.json が生成されます．

## 出力形式

horse_master.json

```
[
    {
        "netkeiba_id" : "10桁の競走馬id",
        "name" : "競走馬名",
        "birthday" : "YYYY年MM月DD日",
        "sex" : 性別(0 : 牡，0.5 : 牝，1 : セ),
        "ped_id" : "血統ID(血統マスタのid)",　　
        "trainer_id" : "10桁の調教師ID",
        "wins" : 勝数(0〜の整数),
        "win_rate" : 直近10件の1位になった率(0〜1の小数),
        "Rank_average" : 直近10件の順位平均,
        "money" : 獲得賞金(0〜の整数),
        "course_suitability" : コース適正(0〜1の小数；0 : 芝 <-> 1 : ダート),
        "distance_suitability" : 距離適正(0〜1の小数；0 : 短 <-> 1 : 長),
        "limb" : 脚質特性(0〜1の小数；0 : 逃げ <-> 1 : 追込),
        "growth" : 成長特性(0〜1の小数；0 : 早熟 <-> 1 : 晩成),
        "muddy_track_suitability" : 重馬場適正(0〜1の小数；0 : 得意 <-> 1 : 苦手),
        "summer_suitability" : 夏適正(夏の勝率の変動；0 : 下，1 : 上),
        "winter_suitability" : 冬適正(冬の勝率の変動；0 : 下，1 : 上),
        "speed" : 直近10件の走る速度 [m/s](タイム合計 / 距離合計),
        "breeding_center" : "産地名"
    },
    {...},
    {...},
    ...
]
```

ただし，取得失敗時，値は null で埋める

### 出力例

horse_master1.json

```
[
    {
        "netkeiba_id" : "2012102013",
        "name" : "キタサンブラック",
        "birthday" : "2012年3月10日",
        "sex" : 0,
        "ped_id" : "",　　
        "trainer_id" : "01110",
        "wins" : 12,
        "win_rate" : 0.6,
        "rank_average" : 2.55,
        "money" : 1876840000,
        "course_suitability" : 0.178571429,
        "distance_suitability" : 0.79166666666,
        "limb" : 0.17261904761,
        "growth" : 0.73809523809,
        "muddy_track_suitability" : 0.26785714285,
        "summer_suitability" : 1,
        "winter_suitability" : 0,
        "speed" : 16.2337662338,
        "breeding_center" : "日高町"
    },
    {...},
    {...},
    ...
]
```
