'''
・現役、引退の騎手idを取得する
・csv形式で保存
'''
import csv
import requests
from bs4 import BeautifulSoup
import scp


def has_duplicates(seq):
    ## -----*----- 配列に重複があるか判別 -----*----- ##
    return len(seq) != len(set(seq))


def get_all_id(url):
    ## -----*----- すべての騎手IDを取得 -----*----- ##
    jockey_id = []
    NUM_PAGE = 28  # 騎手検索結果のページ数

    for i in range(NUM_PAGE):
        print(f'{i+1}ページ目')
        html = scp.get_html(url+str(i+1))

        soup = BeautifulSoup(html, 'html.parser')
        jockey_id.extend(get_id(soup))

    print(has_duplicates(jockey_id))

    return jockey_id


def get_id(soup):
    ## -----*----- 1ページ分の騎手IDを取得 -----*----- ##
    selector = '#contents_liquid > table > tr > td:nth-child(1) > a'

    return [i.get('href')[8:13] for i in soup.select(selector)]


def main():
    JOCKEY_LIST_URL = 'https://db.netkeiba.com/?pid=jockey_list&act[]=0&act[]=1&list=100&page='

    # すべての騎手IDを取得
    id = get_all_id(JOCKEY_LIST_URL)
    print(id)

    # CSV形式で保存
    with open('jockey_id.csv', 'w') as f:
        csv.writer(f).writerow(id)


if __name__ == '__main__':
    main()
