import scp
from bs4 import BeautifulSoup
import re


def get_all_trainer_data(id_list, url):
    ## -----*----- すべての調教師データを辞書型で取得 -----*----- ##
    trainer_data = []
    err_trainer_id = []

    for i in range(len(id_list)):
        print(f'{i} {id_list[i]}')
        try:
            trainer_data.append(get_one_trainer_data(id_list[i], url))
        except:
            err_trainer_id.append(id_list[i])

    print(f'data that couldn\'t be acquired : {err_trainer_id}')

    return trainer_data


def get_one_trainer_data(id, url):
    ## -----*----- １人分の調教師データを辞書型で取得 -----*----- ##
    data = {}

    html = scp.get_html(url + id)
    soup = BeautifulSoup(html, 'html.parser')

    data['netkeiba_id'] = id
    data['name'] = get_trainer_name(soup)

    ranks = get_ranks(soup)
    ranks = remove_NaN(ranks)  # 数字でない着順情報を除去

    data['win_rate'] = get_win_rate(ranks)
    data['rank_average'] = get_rank_average(ranks)

    return data


def get_trainer_name(soup):
    ## -----*----- １ページ分の調教師名を取得 -----*----- ##
    selector = '#db_main_box > div > div.db_head_name.fc > h1'

    name = soup.select_one(selector).text

    # 不要な文字列の削除
    name = name.replace('\n', '').replace(u'\xa0', u'')
    try:
        name = name[:re.search('\(', name).start()]
    except:
        pass

    return name


def get_ranks(soup):
    ## -----*----- 着順を取得 -----*----- ##
    selector = '#contents_liquid > table > tbody > tr > td:nth-child(12)'

    rank = [i.text for i in soup.select(selector)]

    return rank


def remove_NaN(ranks):
    ## -----*----- 数字でない着順を除去 -----*----- ##
    new_ranks = []
    for rank in ranks:
        try:
            new_ranks.append(int(rank))
        except:
            pass
    # print(new_ranks)
    return new_ranks


def get_win_rate(ranks):
    ## -----*----- 勝率を取得 -----*----- ##
    # 近走成績がない調教師
    if len(ranks) == 0:
        return 0

    num_win = 0
    for rank in ranks:
        if rank == 1:
            num_win += 1

    return num_win/len(ranks)


def get_rank_average(ranks):
    ## -----*----- 平均順位を取得 -----*----- ##
    # 近走成績がない調教師
    if len(ranks) == 0:
        return 0

    sum = 0
    for rank in ranks:
        sum += rank

    return sum/len(ranks)
