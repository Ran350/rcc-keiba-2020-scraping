'''
競走馬マスタを取得
'''

import csv
import json
from pprint import pprint
from sys import version

from bs4 import BeautifulSoup
import requests
from time import sleep

from hp import HorseProfile
import hr
import hs


def main():
    version = '1'
    print('version: ' + version)

    id_list = []

    # csvファイルを開いて競走馬IDを取得
    file_name = "./../horse_id/horse_id/horse_id"+version+".csv"
    with open(file_name) as f:
        for row in csv.reader(f):
            id_list = row

    # すべての競走馬idをリストで取得
    horse_data = get_all_horse_data(id_list)
    # pprint(horse_data)

    # json形式に変換し保存
    file_path = '../horse_data/horse_master'+version+'.json'
    with open(file_path, 'w') as f:
        json.dump(horse_data,
                  f,
                  ensure_ascii=False,
                  indent=2,
                  sort_keys=True,
                  separators=(',', ': '))


def get_all_horse_data(id_list: list) -> list:
    ## -----*----- すべての競走馬データを取得 -----*----- ##
    horse_data = []
    err_horse_id = []

    for i in range(len(id_list)):
        try:
            print(f'{i} {id_list[i]}')
            horse_data.append(get_one_horse_data(id_list[i]))

        except:
            # エラーメッセージ表示
            print(id_list[i])
            import traceback
            traceback.print_exc()

            err_horse_id.append(id_list[i])

    print('num of success data: '+str(len(horse_data)))
    print(f'horse id that failed to be acquired : {err_horse_id}')

    return horse_data


def get_one_horse_data(id: list) -> dict:
    ## -----*----- １人分の競走馬データを取得 -----*----- ##
    url = 'https://db.netkeiba.com/horse/'
    html = download_html(url + id)
    soup = BeautifulSoup(html, 'html.parser')

    data = {}

    data['netkeiba_id'] = id
    data['ped_id'] = id

    # プロフィールを取得
    profile = HorseProfile(soup)
    data['name'] = profile.get_name(soup)
    data['sex'] = profile.get_sex(soup)
    data['birthday'] = profile.get_birthday(soup)
    data['trainer_id'] = profile.get_trainer_id(soup)
    data['breeding_center'] = profile.get_breeding_center(soup)
    data['money'] = profile.get_money(soup)
    data['wins'] = profile.get_wins(soup)

    # 適正値を取得
    data['course_suitability'] = hs.get_course_suitability(soup)
    data['distance_suitability'] = hs.get_distance_suitability(soup)
    data['limb'] = hs.get_limb(soup)
    data['growth'] = hs.get_growth(soup)
    data['muddy_track_suitability'] = hs.get_muddy_track_suitability(soup)

    # レース成績を取得
    data['rank_average'] = hr.get_rank_average(soup)
    data['speed'] = hr.get_speed(soup)
    wr = data['win_rate'] = hr.get_win_rate(soup)
    data['summer_suitability'] = hr.get_summer_suitability(soup, wr)
    data['winter_suitability'] = hr.get_winter_suitability(soup, wr)

    return data


def download_html(url):
    ## -----*----- 指定URLのHTML文字列を取得 -----*----- ##
    for i in range(5):
        sleep(0.2)  # 優しさ
        try:
            res = requests.get(url)
            res.raise_for_status()
            return res.content

            #　エンコードに失敗するなら以下を使用する
            # res.encoding = res.apparent_encoding
            # return res.text

        except:
            print(f'{i} this page is not found')
            sleep(2)

    print(url)


if __name__ == '__main__':
    main()
