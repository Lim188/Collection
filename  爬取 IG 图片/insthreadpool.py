import os
import re
import sys
import json
import time
import random
import requests
from hashlib import md5
from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool

url_base = 'https://www.instagram.com/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    # 'cookie': '这里加上自己的cookie'
    'cookie': 'mid=W56GygAEAAHLfAN7uZg1Q50fTPU8; mcd=3; csrftoken=2eGwLWOMckG9rIcG5cO8paXSJJpMkphp; shbid=3113; ds_user_id=3643774408; rur=PRN; csrftoken=2eGwLWOMckG9rIcG5cO8paXSJJpMkphp; sessionid=IGSC464b7c237acd7c034a61e63eaf34be278abfcc98c9f325f61a2c5ea2aed2b126%3AiihicrgDbfc7hsPkZeUaSHvmGOZwHFok%3A%7B%22_auth_user_id%22%3A3643774408%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%223643774408%3AdNPm6V2e2nXioISzT0sEaokubp1RUMig%3Aa12e0ed0e8c5751abc375a378d49a567a7dce5b8c21bbfeae24e88fbcc795df4%22%2C%22last_refreshed%22%3A1538061274.9771537781%7D; urlgen="{\"64.64.108.201\": 36351\054 \"64.64.108.19\": 36351\054 \"64.64.108.105\": 36351}:1g5Y9B:0tJmVBMrWzsMw_oE2oFqZFbmMTQ"'
}


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_json(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求网页json错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)


def get_content(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print('请求照片二进制流错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_urls(html):
    urls = []
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    print('user_id：' + user_id)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            for edge in edges:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
            yield urls
            print(cursor, flag)
    while flag:
        urls = []
        url = uri.format(user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        for info in infos:
            if info['node']['is_video']:
                video_url = info['node']['video_url']
                if video_url:
                    print(video_url)
                    urls.append(video_url)
            else:
                if info['node']['display_url']:
                    display_url = info['node']['display_url']
                    print(display_url)
                    urls.append(display_url)
        yield urls
        print(cursor, flag)
        # time.sleep(4 + float(random.randint(1, 800))/200)    # if count > 2000, turn on
    # return urls


def main(user):
    url = url_base + user + '/'
    html = get_html(url)
    dirpath = r'\{0}'.format(user)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    for urls in get_urls(html):
        try:
            pool = Pool(4)
            contents = pool.map(get_content, urls)
            pool.close()
            pool.join()
            for i, content in enumerate(contents):
                file_path = r'{0}\{1}.{2}'.format(user, md5(content).hexdigest(), urls[i][-3:])
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        # print('正在下载第{0}张： '.format(i) + urls[i], ' 还剩{0}张'.format(len(urls)-i-1))
                        print('正在下载：', urls[i])
                        f.write(content)
                        f.close()
                else:
                    print('第{0}张照片已下载'.format(i))
        except Exception as e:
            print(e)
            print('这组图片视频下载失败')

'''
argv[1]：sys.argv[]是用来获取命令行参数的,
sys.argv[0]表示代码本身文件路径，所以参数从1开始。
Sys.argv[ ]其实就是一个列表，里边的项为用户输入的参数，
关键就是要明白这参数是从程序外部输入的，而非代码本身的什么地方，
要想看到它的效果就应该将程序保存了，从外部来运行程序并给出参数。

'''

if __name__ == '__main__':
    user_name = sys.argv[1]
    start = time.time()
    main(user_name)
    print('Complete!!!!!!!!!!')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'一共花费了{hour}小时{minu}分钟{sec}秒')
