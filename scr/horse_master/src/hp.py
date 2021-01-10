"""
競走馬プロフィール表から取得
"""

from bs4 import BeautifulSoup
from re import findall
from kanji2num import convert_kanji


NON_VAL = None


class HorseProfile():
    def __init__(self, soup):
        self.is_recruit_info = self.check_recruit_info(soup)

    def check_recruit_info(self, soup) -> int:
        ## -----*----- 募集者情報がある表か確認する -----*----- ##
        # もしあれば産地名，獲得賞金，通算成績の行が1行ずれる
        selector = '#owner_info_tr > th'

        # 募集者情報がなかった
        if soup.select_one(selector) == None:
            return 0

        # 募集者情報があった
        # print('this page has recruitment infomation')
        return 1

    def get_name(self, soup):
        ## -----*----- 競走馬名を取得 -----*----- ##
        name = soup.title.text
        return name[:name.find('|') - 1]  # 競走馬名以外の文字列は削除

    def get_sex(self, soup):
        ## -----*----- 性別を取得 -----*----- ##
        selector = '#db_main_box > div.db_head.fc > div.db_head_name.fc > div.horse_title > p.txt_01'
        text = soup.select_one(selector).text  # 例: "抹消　牡　鹿毛"

        if '牡' in text:
            return 0
        if '牝'in text:
            return 0.5
        if 'セ'in text:
            return 1
        return NON_VAL  # 取得に失敗

    def get_birthday(self, soup):
        ## -----*----- 誕生日を取得 -----*----- ##
        selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child(1) > td'
        return soup.select_one(selector).text

    def get_trainer_id(self, soup):
        ## -----*----- 調教師IDを取得 -----*----- ##
        selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child(2) > td > a'
        tag = soup.select_one(selector)

        if tag == None:  # 調教師IDが存在しない
            return NON_VAL

        href = tag.get('href')  # 例: "/trainer/12345/"
        return href[9:-1]  # 例: "12345"

    def get_breeding_center(self, soup):
        ## -----*----- 産地名を取得 -----*----- ##
        selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child('\
            + str(5+self.is_recruit_info)+') > td'
        # 募集情報の行がある表では産地名の行は１行下

        return soup.select_one(selector).text  # 例: "日高町"

    def get_money(self, soup):
        ## -----*----- 獲得賞金を取得 -----*----- ##
        # 募集情報の行がある表では獲得賞金の行は１行下
        selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child('\
            + str(7+self.is_recruit_info)+') > td'

        tag = soup.select_one(selector).text  # 例: "\n\n\n18億7,684万円 (中央)\n"
        colum = tag.replace('\n', '')         # 例: "18億7,684万円 (中央)"
        money = colum[:colum.find('円')]      # 例: "18億7,684万"
        return convert_kanji(money)           # 例: 1876840000

    def get_wins(self, soup):
        ## -----*----- 勝数を取得 -----*----- ##
        selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child('\
            + str(8+self.is_recruit_info)+') > td'
        # 募集情報の行がある表では通算成績の行は１行下

        record = soup.select_one(selector).text  # 例: "20戦12勝 [12-2-4-2]"
        wins = findall('戦.*?勝', record)[0].strip('戦勝')  # 例: "12"

        return int(wins)
