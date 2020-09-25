'''
・現役、引退の騎手idを取得する
・csv形式で保存
'''
import csv
from bs4 import BeautifulSoup
import scp


def has_duplicates(seq):
    ## -----*----- 配列に重複があるか判別 -----*----- ##
    return len(seq) != len(set(seq))


def get_all_id(url):
    ## -----*----- すべての調教師IDを取得 -----*----- ##
    trainer_id = []
    NUM_PAGE = 23  # 調教師検索結果のページ数

    for i in range(NUM_PAGE):
        print(f'{i+1}ページ目')
        html = scp.get_html(url+str(i+1))

        soup = BeautifulSoup(html, 'html.parser')
        trainer_id.extend(get_id(soup))

    print(has_duplicates(trainer_id))
    print(trainer_id)

    return trainer_id


def get_id(soup):
    ## -----*----- 1ページ分の調教師IDを取得 -----*----- ##
    selector = '#contents_liquid > table > tr > td:nth-child(1) > a'

    return [i.get('href')[9:14] for i in soup.select(selector)]


def main():
    trainer_list_url = 'https://db.netkeiba.com/?pid=trainer_list&bel[]=1&bel[]=2&bel[]=3&bel[]=4&list=100&page='

    # すべての騎手IDを取得
    id = get_all_id(trainer_list_url)
    print(id)

    # CSV形式で保存
    with open('trainer_id.csv', 'w') as f:
        csv.writer(f).writerow(id)


if __name__ == '__main__':
    main()
