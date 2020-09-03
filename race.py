# 1回分のレースデータを取得
'''
get_race_data(base_url,race_ids)
    get_one_race_data(base_url,race_id)
        get_race_ground(soup)
        get_race_distance(soup)
        get_race_weather(soup)
        get_horse_data(soup)
'''

from bs4 import BeautifulSoup
import re
from pprint import pprint
import horse
import scp


def get_race_data(base_url, race_ids):
    ## -----*----- すべてのレースデータを取得 -----*----- ##
    race_data = []

    for i in range(len(race_ids)):
        print(i)
        race_data.append({})

        # 各レースデータ取得
        race_data[i] = get_one_race_data(base_url, race_ids[i])

    result = {}
    result['racedata'] = race_data

    return result


def get_one_race_data(base_url, race_id):
    ## -----*----- 1レースのデータを取得 -----*----- ##
    # HTMLを取得
    if ' ' in race_id:
        race_id = race_id.replace(' ', '')
    print(base_url + race_id)
    html = scp.get_html(base_url + race_id)

    # HTML解析
    soup = BeautifulSoup(html, 'html.parser')

    # 辞書型で初期化
    one_race_data = {}

    # レースデータを取得
    # one_race_data['netkeiba_id'] = race_id
    # one_race_data['name'] = get_race_name(soup)
    one_race_data['馬場状態'] = get_race_ground(soup)
    one_race_data['距離'] = get_race_distance(soup)
    one_race_data['天気'] = get_race_weather(soup)
    one_race_data['競走馬'] = get_horse_data(soup)

    # pprint(one_race_data)
    return one_race_data


def get_race_name(soup):
    ## -----*----- レース名を取得 -----*----- ##
    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > h1'

    return soup.select_one(css_selecter).text


def get_race_ground(soup):
    ## -----*----- 馬場状態を取得 -----*----- ##

    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span'
    data = soup.select_one(css_selecter).text

    if '芝' in data:
        return '芝'
    if 'ダ' in data:
        return 'ダート'
    else:
        return None


def get_race_weather(soup):
    ## -----*----- 天気を取得 -----*----- ##

    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span'
    data = soup.select_one(css_selecter).text

    if '晴' in data:
        return '晴'
    elif '曇' in data:
        return '曇'
    elif '雨' in data:
        return '雨'
    else:
        return None


def get_race_distance(soup):
    ## -----*----- 走距離を取得 -----*----- ##
    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span'

    data = soup.select_one(css_selecter).text

    num = re.sub("\\D", "", data)

    return int(num[:4])


def get_horse_data(soup):
    ## -----*----- 競走馬データを取得 -----*----- ##
    horse_data = []

    # レース結果表を取得
    css_selecter = '.race_table_01 > tr'
    table = soup.select(css_selecter)

    # 競走馬成績を取得
    # horse_id = horse.get_horse_id(soup)
    # number = horse.get_number(soup)
    # trainer_id = horse.get_trainer_id(soup)
    # jockey_id = horse.get_jockey_id(soup)
    # popularity = horse.get_popularity(soup)

    frame = horse.get_frame(soup)
    sex = horse.get_sex(soup)
    age = horse.get_age(soup)
    odds = horse.get_odds(soup)
    weight = horse.get_weight(soup)
    weight_diff = horse.get_weight_diff(soup)
    weight_amount = horse.get_weight_amount(soup)

    # 競走馬成績を辞書に登録
    for rank in range(len(table)-1):  # 1行目は見出し行
        # 辞書型で初期化
        horse_data.append(0)
        horse_data[rank] = {}

        # 登録
        # horse_data[rank]['horse_id'] = horse_id[rank]
        # horse_data[rank]['number'] = number[rank]
        # horse_data[rank]['trainer_id'] = trainer_id[rank]
        # horse_data[rank]['jockey_id'] = jockey_id[rank]
        # horse_data[rank]['popularity'] = popularity[rank]

        horse_data[rank]['枠'] = frame[rank]
        horse_data[rank]['性別'] = sex[rank]
        horse_data[rank]['年齢'] = age[rank]
        horse_data[rank]['順位'] = rank+1
        horse_data[rank]['単勝オッズ'] = odds[rank]
        horse_data[rank]['体重'] = weight[rank]
        horse_data[rank]['体重増減'] = weight_diff[rank]
        horse_data[rank]['斤量'] = weight_amount[rank]

    return horse_data
