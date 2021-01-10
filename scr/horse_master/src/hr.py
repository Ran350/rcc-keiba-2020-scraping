"""
競走成績表から取得
"""

from bs4 import BeautifulSoup


NON_VAL = None


def get_rank_average(soup):
    ## -----*----- 直近20件の順位平均を取得 -----*----- ##
    selector = '#contents > div.db_main_race.fc > div > table > tbody > tr > td:nth-child(12)'

    ranks = []
    for t in soup.select(selector):
        try:
            rank = int(t.text)
            ranks.append(rank)
        except ValueError:  # 順位が数値でない(失,降など)
            pass

    if len(ranks) == 0:
        return NON_VAL  # 出場レースの記録がない

    return sum(ranks)/len(ranks)


def get_win_rate(soup):
    ## -----*----- 直近20件の勝率を取得 -----*----- ##
    selector = '#contents > div.db_main_race.fc > div > table > tbody > tr > td:nth-child(12)'

    ranks = []
    wins = 0  # １着の総数

    for t in soup.select(selector):
        try:
            rank = int(t.text)
            ranks.append(rank)
            if rank == 1:
                wins += 1
        except ValueError:  # 順位が数値でない(失,降など)
            pass

    if len(ranks) == 0:  # 出場レースの記録がない
        return NON_VAL

    return wins/len(ranks)


def get_speed(soup):
    ## -----*----- 直近20件の走る速度を取得 -----*----- ##
    # 距離(m)を取得
    selector = '#contents > div.db_main_race.fc > div > table > tbody > tr > td:nth-child(15)'
    distances = [int(t.text[1:])for t in soup.select(selector)]

    # タイム(分)を取得
    i = check_time_position(soup)
    selector = '#contents > div.db_main_race.fc > div > table > tbody > tr > '\
        'td:nth-child('+str(17+i)+')'    # 馬場指数カラムのある表ではタイムカラムは1列ずれる
    time_min = [t.text for t in soup.select(selector)]  # 例: ["2:33.6",...]

    # 各レースの速度(m/s)を算出
    speeds = []
    for i in range(len(time_min)):
        try:
            # タイム(秒)を算出
            t = time_min[i]
            min = int(t[:t.find(':')])  # 例: 2
            sec = int(t[t.find(':')+1:t.find('.')])  # 例: 33
            msec = int(t[t.find('.')+1:])  # 例: 6
            time_sec = 60 * min + sec + 0.1 * msec

            # 速度(m/s)を算出
            speeds.append(distances[i]/time_sec)

        except ValueError:
            pass

    if len(speeds) == 0:  # 出場レースの記録がない
        return NON_VAL

    # 平均速度(m/s)を算出
    return sum(speeds)/len(speeds)


def check_time_position(soup) -> int:
    selector = '#contents > div.db_main_race.fc > div > table > thead > tr > th:nth-child(17)'
    text = soup.select_one(selector).text
    if text == 'タイム':
        return 0
    return 1


def get_summer_suitability(soup, year_win_rate: float) -> int:
    ## -----*----- 夏適正を取得 -----*----- ##
    return get_season_suitability('summer', soup, year_win_rate)


def get_winter_suitability(soup, year_win_rate: float) -> int:
    ## -----*----- 冬適正を取得 -----*----- ##
    return get_season_suitability('winter', soup, year_win_rate)


def get_season_suitability(season: str, soup, year_win_rate: float) -> int:
    ## -----*----- 各季節の適正を取得 -----*----- ##
    # 着順を取得
    ranks = []
    selector = '#contents > div.db_main_race.fc > div > table > tbody > tr > td:nth-child(12)'
    for t in soup.select(selector):
        try:
            rank = int(t.text)
            ranks.append(rank)
        except ValueError:  # 順位が数値でない(失,降など)
            ranks.append(None)

    # 試合月を取得
    monthes = []
    selector = '#contents > div.db_main_race.fc > div > table > tbody > tr > td:nth-child(1) > a'
    for t in soup.select(selector):
        try:
            date = t.text  # 例: '2000/06/03'
            month = int(date[5:7])  # 例: 6
            monthes.append(month)
        except ValueError:  # 順位が数値でない(失,降など)
            ranks.append(None)

    target_month = {'summer': [7, 8, 9],
                    'winter': [12, 1, 2]}

    # 夏or冬の勝利数を算出
    season_game_num = 0  # 夏/冬の試合数
    season_win_num = 0  # 夏/冬の１着の総数
    for i in range(len(monthes)):
        if monthes[i] in target_month[season]:
            season_game_num += 1
            if ranks[i] == 1:
                season_win_num += 1

    # 一度も夏/冬にレースがなかった場合
    if season_game_num == 0:
        return NON_VAL

    # 夏or冬の勝率
    season_win_rate = season_win_num / season_game_num

    if season_win_rate > year_win_rate:
        return 1
    return 0
