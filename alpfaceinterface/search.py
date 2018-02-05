# -*- coding: utf-8 -*-
# @Time    : 1/19/18 6:28 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : search.py
# @Software: PyCharm

import re
import urllib.request
from multiprocessing import Pool
from urllib.request import urlopen
import random
import os

from bs4 import BeautifulSoup

default_max_wait_time = 3  # 默认最大等待时间3秒

option_split_word = ['的', '之', '、', '和']

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'

# Load the list of valid user agents from the install folder.
install_folder = os.path.abspath(os.path.split(__file__)[0])
user_agents_file = os.path.join(install_folder, 'user_agents.txt')
try:
    with open(user_agents_file) as fp:
        user_agents_list = [_.strip() for _ in fp.readlines()]
except Exception:
    user_agents_list = [USER_AGENT]


def search(question, option_arr, is_negative):
    currentSearch = {}
    wd = urllib.request.quote(question)
    pool = Pool()
    source_1 = pool.apply_async(search_baidu, args=(wd, option_arr))
    source_2 = pool.apply_async(search_zhidao, args=(wd, option_arr))
    pool.close()
    # pool.join()
    source_arr, baidu_url, baiduzhidao_url = get_source(source_1, source_2)
    print('分数统计是：{}'.format(source_arr))
    best_answer, best_index = get_result(source_arr, option_arr, is_negative)
    currentSearch['baidu_url'] = baidu_url
    currentSearch['baiduzhidao_url'] = baiduzhidao_url
    if best_answer is not None or best_answer != '':
        currentSearch['best_answer'] = best_answer
        currentSearch['best_index'] = best_index
        currentSearch['best_answer_index'] = option_arr.index(best_answer)
    else:
        currentSearch['best_answer'] = ''
        currentSearch['best_index'] = 0
        option_arr['best_answer_index'] = -1
    return currentSearch
    #return best_answer, best_index

def google_search(question, option_arr, is_negative):
    currentSearch = {}
    wd = urllib.request.quote(question)
    pool = Pool()
    source = pool.apply_async(search_google, args=(wd, option_arr))
    pool.close()
    # pool.join()

    source_arr, google_url = get_google_source(source)
    print('分数统计是：{}'.format(source_arr))
    best_answer, best_index = get_result(source_arr, option_arr, is_negative)
    currentSearch['google_url'] = google_url
    if best_answer is not None or best_answer != '':
        currentSearch['best_answer'] = best_answer
        currentSearch['best_index'] = best_index
        currentSearch['best_answer_index'] = option_arr.index(best_answer)
    else:
        currentSearch['best_answer'] = ''
        currentSearch['best_index'] = 0
        option_arr['best_answer_index'] = -1
    return currentSearch



# 百度搜索
def search_baidu(question, option_arr):
    result_list = []
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    head = {}
    head['User-Agent'] = user_agent
    url = 'https://www.baidu.com/s?wd={}'.format(question)
    print(url)
    request = urllib.request.Request(url, headers=head)
    result = urlopen(request)
    body = BeautifulSoup(result.read(), 'html5lib')
    content_list = body.find('div', id='content_left')
    if content_list is None:
        return [0, 0, 0], url
    content_list = content_list.findAll('div')
    # print(content_list)
    for content in content_list:
        content_text = content.get_text()
        content_text = re.sub('\s', '', content_text)
        result_list.append(content_text)
    answer_num = len(result_list)
    source_arr = []
    op_num = len(option_arr)
    for i in range(0, op_num):
        source_arr.append(0)
    for i in range(0, answer_num):
        result = result_list[i]
        for j in range(0, op_num):
            op = option_arr[j]
            if op in result:  # 选项在答案中出现一次，加10分
                source_arr[j] += 5
    return source_arr, url

# Google 搜索
def search_google(question, option_arr):
    result_list = []
    header = {}
    header['User-Agent'] = USER_AGENT
    # url = "https://www.google.co.jp/search?source=hp&q={question}".format(
    #     question=question,
    # )

    url = "https://{domain}/search?hl={language}&q={query}&btnG=Search&gbv=1".format(
        domain = "www.google.co.jp", language='en', query=question
    )
    print(url)
    request = urllib.request.Request(url=url, headers=header)
    result = urlopen(request)
    soup = BeautifulSoup(result.read(), 'html5lib')
    content_list = soup.find(id='search')
    if content_list is None:
        return [0, 0, 0], url
    content_list = content_list.findAll('div')
    if content_list is None:
        return [0, 0, 0], url
    for content in content_list:
        content_text = content.get_text()
        content_text = re.sub("\s", '', content_text)
        result_list.append(content_text)
    answer_num = len(result_list)
    source_arr = []
    op_num = len(option_arr)
    for v in range(0, op_num):
        source_arr.append(0)
    for i in range(0, answer_num):
        res = result_list[i]
        for j in range(0, op_num):
            op = option_arr[j]
            if op in res:
                source_arr[j] += 5
    return source_arr, url

# 百度知道搜题
def search_zhidao(question, option_arr):
    result_list = []
    url = 'https://zhidao.baidu.com/search?word={}'.format(
        question)
    print(url)
    result = urlopen(url)
    # 解析页面
    body = BeautifulSoup(result.read(), 'html5lib')
    good_result_div = body.find(class_='list-header').find('dd')
    second_result_div = body.find(class_='list-inner').find(class_='list')
    if good_result_div is not None:
        good_result = good_result_div.get_text()
        result_list.append(good_result)

    if second_result_div is not None:
        second_result_10 = second_result_div.findAll('dl')  # .find(class_='answer').get_text()
        if second_result_10 is not None and len(second_result_10) > 0:
            for each_result in second_result_10:
                result_dd = each_result.get_text()
                result_text = re.sub('\s', '', result_dd)
                result_list.append(result_text)
                print(result_text)
    answer_num = len(result_list)
    source_arr = []
    op_num = len(option_arr)
    for i in range(0, op_num):
        source_arr.append(0)
    for i in range(0, answer_num):
        result = result_list[i]
        for j in range(0, op_num):
            op = option_arr[j]
            op_arr = split_option(op)  # 对选项进行简单分词搜索，如
            if op_arr is not None:
                for op_wd in op_arr:
                    if op_wd in result:
                        source_arr[j] += 5
            if op in result:  # 选项在答案中出现一次，加10分
                source_arr[j] += 10
                if re.search('[答案|结果|而是].{4}' + op, result) is not None:
                    source_arr[j] += 20
    return source_arr, url


def get_result(source_arr, option_arr, is_negate):
    if len(source_arr) == 0 or max(source_arr) == 0:
        return None
    if is_negate:
        best_index = min(source_arr)
    else:
        best_index = max(source_arr)
    best_result = option_arr[source_arr.index(best_index)]
    for num in source_arr:
        print(num)
    return best_result, best_index


def get_source(source_1, source_2):
    s1, s2 = [], []
    url1, url2 = '', ''
    try:
        s1, url1 = source_1.get(default_max_wait_time)
    except BaseException as ex:
        print(ex)
        s1 = [0, 0, 0]
    try:
        s2, url2 = source_2.get(default_max_wait_time)
    except BaseException as ex:
        print(ex)
        s2 = [0, 0, 0]
    print('百度网页搜索结果:{}'.format(s1))
    print('百度知道结果：{}.'.format(s2))
    source_arr = over_add(s1, s2)
    return source_arr, url1, url2

def get_google_source(source):
    s1 = []
    url1 = ''
    try:
        s1, url1 = source.get(default_max_wait_time)
    except BaseException as ex:
        print(ex)
        s1 = [0, 0, 0]
    print('Google搜索结果:{}'.format(s1))
    return s1, url1


def over_add(arr1, arr2):
    length = min(len(arr1), len(arr2))
    arr = []
    for i in range(0, length):
        arr.append(0)
    for i in range(length):
        arr[i] = arr1[i] + arr2[i]
    return arr

def split_option(option):
    option_arr = []
    for wd in option_split_word:
        option_arr = option.split(wd)
        if len(option_arr) > 1:
            break
    if len(option_arr) > 1:
        return option_arr
    else:
        return None


# Get a random user agent.
def get_random_user_agent():
    """
    Get a random user agent string.

    @rtype:  str
    @return: Random user agent string.
    """
    return random.choice(user_agents_list)
