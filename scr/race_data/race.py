'''
レースデータを取得

get_race_data(base_url,race_ids)
    get_one_race_data(base_url,race_id)
        get_name(soup)
        get_race_ground(soup)
        get_turn(soup)
        get_race_distance(soup)
        get_race_weather(soup)
        get_date(soup)
        get_prize_money(soup)
        get_horse_data(soup)
'''

from bs4 import BeautifulSoup
import re
import horse
import scp


def get_race_data(base_url, id_list):
    ## -----*----- すべてのレースデータを取得 -----*----- ##
    race_data = []
    err_id = []

    for i in range(len(id_list)):
        print(f'{i} {id_list[i]}')
        race_data.append({})

        # 各レースデータ取得
        try:
            race_data[i] = get_one_race_data(base_url, id_list[i])
        except:
            err_id.append(id_list[i])

    print(f'data that couldn\'t be acquired : {err_id}')

    return race_data  # result


def get_one_race_data(base_url, race_id):
    ## -----*----- 1レースのデータを取得 -----*----- ##
    # 謎のスペースを削除
    if ' ' in race_id:
        race_id = race_id.replace(' ', '')

    # HTMLを取得
    html = scp.get_html(base_url + race_id)

    # HTML解析
    soup = BeautifulSoup(html, 'html.parser')

    # 辞書型で初期化
    one_race_data = {}

    # レースデータを取得
    one_race_data['netkeiba_id'] = race_id
    one_race_data['レース名'] = get_name(soup)
    one_race_data['馬場状態'] = get_race_ground(soup)
    one_race_data['周り方'] = get_turn(soup)
    one_race_data['距離'] = get_race_distance(soup)
    one_race_data['天気'] = get_race_weather(soup)
    one_race_data['開催日'] = get_date(soup)
    one_race_data['賞金'] = get_prize_money(soup)
    one_race_data['競走馬'] = get_horse_data(soup)

    return one_race_data


def get_name(soup):
    ## -----*----- レース名を取得 -----*----- ##
    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > h1'

    name = soup.select_one(css_selecter).text

    return name


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


def get_turn(soup):
    ## -----*----- 周り方を取得 -----*----- ##
    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span'
    data = soup.select_one(css_selecter).text

    if '右' in data:
        return '右'
    if '左' in data:
        return '左'
    else:
        return None


def get_race_distance(soup):
    ## -----*----- 走距離を取得 -----*----- ##
    css_selecter = '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span'

    data = soup.select_one(css_selecter).text

    num = re.sub("\\D", "", data)

    return int(num[:4])


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


def get_date(soup):
    ## -----*----- 開催日を取得 -----*----- ##
    css_selecter = '#main > div > div > div > ul > li.result_link > a'

    date = soup.select_one(css_selecter).text

    return date[:11]  # "2019年09月01日のレース結果"の11文字目まで取得


def get_prize_money(soup):
    ## -----*----- 賞金を取得 -----*----- ##
    table_css_selecter = '.race_table_01'
    prize_css_selecter = 'table > tr > td:nth-child(21)'

    table = soup.select_one(table_css_selecter)

    # tableから<diary_snap_cut>タグを除去
    table = scp.rm_both_tag(str(table), 'diary_snap_cut')
    table = BeautifulSoup(table, 'html.parser')

    prizes = table.select(prize_css_selecter)

    # int型の賞金を配列で返す
    result = []
    for i in prizes:
        if(i.text == ''):
            return result

        # str型の"5.0"は直接intにキャストできない
        result.append(10000*int(float(i.text.replace(',', ''))))


def get_horse_data(soup):
    ## -----*----- 競走馬データを取得 -----*----- ##
    horse_data = []  # 競走馬データ

    # レース結果表を取得
    css_selecter = '.race_table_01 > tr'
    table = soup.select(css_selecter)

    # 競走馬成績を取得
    horse_id = horse.get_horse_id(soup)
    # frame = horse.get_frame(soup)
    number = horse.get_number(soup)
    sex = horse.get_sex(soup)
    age = horse.get_age(soup)
    weight_amount = horse.get_weight_amount(soup)
    # jockey_id = horse.get_jockey_id(soup)
    odds = horse.get_odds(soup)
    # popularity = horse.get_popularity(soup)
    weight = horse.get_weight(soup)
    weight_diff = horse.get_weight_diff(soup)
    # trainer_id = horse.get_trainer_id(soup)

    # 競走馬成績を辞書に登録
    for rank in range(len(table)-1):  # 1行目は見出し行
        # 辞書型で初期化
        horse_data.append(0)
        horse_data[rank] = {}

        # 登録
        horse_data[rank]['競走馬ID'] = horse_id[rank]
        horse_data[rank]['順位'] = rank+1
        # horse_data[rank]['枠'] = frame[rank]
        # horse_data[rank]['jockey_id'] = jockey_id[rank]
        horse_data[rank]['馬番'] = number[rank]
        horse_data[rank]['性別'] = sex[rank]
        horse_data[rank]['年齢'] = age[rank]
        horse_data[rank]['斤量'] = weight_amount[rank]
        horse_data[rank]['単勝オッズ'] = odds[rank]
        # horse_data[rank]['人気'] = popularity[rank]
        horse_data[rank]['体重'] = weight[rank]
        horse_data[rank]['体重増減'] = weight_diff[rank]
        # horse_data[rank]['trainer_id'] = trainer_id[rank]

    return horse_data
