"""
適性レビュー表から取得
"""

from bs4 import BeautifulSoup


def get_course_suitability(soup):
    ## -----*----- コース適正を取得 -----*----- ##
    selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_01 > div.db_prof_box > dl > dd > table > tr:nth-child(1) > td > img'
    return get_ratio(soup, selector)  # "苦手"の割合


def get_distance_suitability(soup):
    ## -----*----- 距離適性を取得 -----*----- ##
    selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_01 > div.db_prof_box > dl > dd > table > tr:nth-child(2) > td > img'
    return get_ratio(soup, selector)  # "長い"の割合


def get_limb(soup):
    ## -----*----- 脚質特性を取得 -----*----- ##
    selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_01 > div.db_prof_box > dl > dd > table > tr:nth-child(3) > td > img'
    return get_ratio(soup, selector)  # "追い込み"の割合


def get_growth(soup):
    ## -----*----- 成長特性を取得 -----*----- ##
    selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_01 > div.db_prof_box > dl > dd > table > tr:nth-child(4) > td > img'
    return get_ratio(soup, selector)  # "晩成"の割合


def get_muddy_track_suitability(soup):
    ## -----*----- 重馬場適正を取得 -----*----- ##
    selector = '#db_main_box > div.db_main_deta > div > div.db_prof_area_01 > div.db_prof_box > dl > dd > table > tr:nth-child(5) > td > img'
    return get_ratio(soup, selector)  # "苦手"の割合


def get_ratio(soup, selector: str) -> float:
    width = [int(i.attrs['width']) for i in soup.select(selector)]
    return (width[3]+width[4])/(sum(width)-1)  # width[3]と[4]が対象のwidth値
