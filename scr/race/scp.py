import requests
import bs4
from time import sleep


def get_html(url):
    ## -----*----- 指定URLのHTML文字列を取得 -----*----- ##
    err = 0
    while True:
        try:
            res = requests.get(url)
            res.raise_for_status()
            sleep(0.1)  # 優しさ
            break
        except:
            err += 1
            print(str(err) + ' this page is not found ')
            sleep(1)
            if err == 10:
                break
    return res.content


def get_href(soup, css_selecter):
    ## -----*----- CSSセレクタで指定したaタグのhrefの値を取得 -----*----- ##
    links = [i.get('href') for i in soup.select(css_selecter)]

    return links


def rm_tag(html, tag):
    ## -----*----- 指定タグ両方除去 -----*----- ##

    while True:
        num = html.find(tag)
        if num == -1:
            break
        html = html[:num] + html[num + len(tag):]

    return html


def rm_both_tag(html, tag):
    ## -----*----- 開始タグ終了タグ両方除去 -----*----- ##
    html = rm_tag(html, '<' + tag + '>')
    html = rm_tag(html, '</' + tag + '>')

    return html
