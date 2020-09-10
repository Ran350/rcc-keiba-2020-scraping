# 軽量版レースデータ収集


RCC 2020 年度競馬 AI 班　スクレイピング係

## 概要

軽量版レースデータを収集する．
json形式で出力する.

## 実行環境

- Python ~> 3.7
- requests 2.22.0
- beautifulsoup4 4.8.2

## 準備
```sh
git clone <this repo>
cd <this repo>
```

- 各年度のレースIDを記述したCSVファイルをrace_idディレクトリに用意する

- 実行ファイルmain.py中のmain()内にある，変数yearに収集年度の西暦を，文字列型で指定する．
```
def main():
    ...
    year = '2020'
```

## 実行
```sh
python main.py
```

## 出力データの仕様

- 欠損値には 0 を入れる

### 出力形式
race_data_2020.json
```
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
            ...(その他の競走馬データ)...
        }
      ]
    },
    {
        ...(その他のレースデータ)...
    }
  ]
}
```

### 出力例
<https://github.com/Ran350/get-race-data/blob/master/race_data/race_data_2020.json>

## 引用
<https://db.netkeiba.com/>

## 作成者

- [Ran350](https://github.com/Ran350)
