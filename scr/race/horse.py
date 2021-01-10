# 各順位の競走馬の列データを取得

'''
get_frame(soup)
get_sex(soup)
get_age(soup)
get_horse_id(soup)
get_number(soup)
get_trainer_id(soup)
get_jockey_id(soup)
get_odds(soup)
get_popularity(soup)
get_weight(soup)
get_weight_diff(soup)
get_weight_amount(soup)
'''

from bs4 import BeautifulSoup
import scp


def get_frame(soup):
    ## -----*----- 枠取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(2)'
    frame = [int(i.text) for i in soup.select(css_selecter)]
    return frame


def get_number(soup):
    ## -----*----- 馬番取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(3)'

    return [int(i.text) for i in soup.select(css_selecter)]


def get_sex(soup):
    ## -----*----- 性別取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(5)'
    sex = [i.text[0] for i in soup.select(css_selecter)]
    return sex


def get_age(soup):
    ## -----*----- 年齢取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(5)'
    age = [int(i.text[1:]) for i in soup.select(css_selecter)]
    return age


def get_horse_id(soup):
    css_selecter = '.race_table_01 > tr > td:nth-child(4) > a'
    horse_ids = scp.get_href(soup, css_selecter)

    # URLからidだけを抽出
    return [id[7:17] for id in horse_ids]


def get_trainer_id(soup):
    ## -----*----- 調教師id取得 -----*----- ##
    table_css_selecter = '.race_table_01'
    trainer_css_selecter = 'table > tr > td:nth-child(19) > a'

    table = soup.select_one(table_css_selecter)

    # tableから<diary_snap_cut>タグを除去
    table = scp.rm_both_tag(str(table), 'diary_snap_cut')
    table = BeautifulSoup(table, 'html.parser')

    trainer_ids = scp.get_href(table, trainer_css_selecter)

    # '/trainer/01136/'の9〜13文字目のidを抽出
    return [id[9:14] for id in trainer_ids]


def get_jockey_id(soup):
    ## -----*----- 騎手id取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(7) > a'
    jockey_ids = scp.get_href(soup, css_selecter)

    # '/jockey/01180/'の9〜13文字目のidを抽出
    return [id[8:13] for id in jockey_ids]


def get_odds(soup):
    ## -----*----- 単勝取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(11)'
    odds = soup.select(css_selecter)
    for i in range(len(odds)):
        try:
            odds[i] = float(odds[i].text)
        except:  # データがないとき
            odds[i] = 0

    return odds


def get_popularity(soup):
    ## -----*----- 人気取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(12)'
    popularity = soup.select(css_selecter)
    for i in range(len(popularity)):
        try:
            popularity[i] = int(popularity[i].text)
        except:  # oddsが'___'のとき
            popularity[i] = 0

    return popularity


def get_weight(soup):
    ## -----*----- 馬体重取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(13)'
    weight = soup.select(css_selecter)

    #  # '512(+6)'の馬体重の部分のみ抽出
    for i in range(len(weight)):
        try:
            weight[i] = int(weight[i].text[:3])
        except:  # データがないとき
            weight[i] = 0

    return weight


def get_weight_diff(soup):
    ## -----*----- 馬体重増減取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(13)'
    weight = soup.select(css_selecter)

    #  # '512(+6)'の馬体重増減の部分のみ抽出
    for i in range(len(weight)):
        try:
            weight[i] = int(weight[i].text[4:-1])
        except:  # データがないとき
            weight[i] = 0

    return weight


def get_weight_amount(soup):
    ## -----*----- 斤量取得 -----*----- ##
    css_selecter = '.race_table_01 > tr > td:nth-child(6)'
    weight_amount = [float(i.text) for i in soup.select(css_selecter)]
    return weight_amount
