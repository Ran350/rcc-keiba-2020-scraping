'''
競走馬IDを獲得賞金が大きい順に5000件ごとに取得する
csv形式で１行で保存
'''

import csv
import requests
from bs4 import BeautifulSoup
from time import sleep


def main():
    for version in range(1, 10):
        # すべての競走馬IDを取得
        id = get_all_id(version)
        # print(id)
        print(len(id))

        # CSV形式で保存
        file_path = 'horse_id/horse_id'+str(version)+'.csv'
        with open(file_path, 'w') as f:
            csv.writer(f).writerow(id)


def get_all_id(verssion):
    ## -----*----- すべての競走馬IDを取得 -----*----- ##
    url = 'https://db.netkeiba.com/?pid=horse_list&grade[]=1&grade[]=2&grade[]=3&list=100&page='
    first_page = (verssion-1) * 50 + 1  # 5000件(50ページ)ごと
    last_page = first_page + 50

    print(first_page, last_page)

    jockey_id = []
    for i in range(int(first_page), int(last_page)):
        print(f'{i}ページ目')
        html = download_html(url + str(i))
        parsed_html = BeautifulSoup(html, 'html.parser')
        id = extract_id(parsed_html)
        jockey_id.extend(id)

    return jockey_id


def extract_id(soup):
    ## -----*----- HTMLから1ページ分の競走馬IDを抽出 -----*----- ##
    # なぜかCSSセレクタではtableタグが抽出できなかった
    table_tag = soup.find("table")

    selector = 'tr > td:nth-child(2) > a'
    a_tags = table_tag.select(selector)

    return [i.get('href')[7:-1] for i in a_tags]  # href="/horse/123456789A/"


def download_html(url):
    ## -----*----- 指定URLのHTML文字列を取得 -----*----- ##
    for i in range(10):
        sleep(3)  # 優しさ
        try:
            res = requests.get(url)
            res.raise_for_status()
            return res.content

        except:
            print(str(i) + ' this page is not found')

    print(url)


if __name__ == '__main__':
    main()
