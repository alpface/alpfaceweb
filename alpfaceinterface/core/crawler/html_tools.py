# -*- coding: utf-8 -*-
# @Time    : 1/18/18 7:14 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : html_tools.py
# @Software: PyCharm

import re
import urllib

import requests
from bs4 import BeautifulSoup

'''
获取百度知道的页面
'''


def get_html_zhidao(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_zhidao = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_zhidao(['script', 'style', 'img'])]
    # print(soup.prettify())
    return soup_zhidao


'''
获取百度百科的页面
'''


def get_html_baike(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_baike = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_baike(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup.prettify())
    return soup_baike


'''
获取Bing网典的页面
'''


def get_html_bingwd(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_bingwd = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_bingwd(['script', 'style', 'img', 'sup', 'b'])]
    # print(soup.prettify())
    return soup_bingwd


'''
获取百度搜索的结果
'''


def get_html_baidu(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
    soup_baidu = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")

    # 去除无关的标签
    [s.extract() for s in soup_baidu(['script', 'style', 'img'])]
    # print(soup.prettify())
    return soup_baidu


'''
获取Bing搜索的结果
'''


def get_html_bing(url):
    # url = 'http://global.bing.com/search?q='+word
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    soup_bing = BeautifulSoup(requests.get(url=url, headers=headers).content.decode('utf-8'), "lxml")

    # 去除无关的标签
    # [s.extract() for s in soup_bing(['script', 'style','img'])]
    return soup_bing


'''
print answer
'''


def ptranswer(ans, ifhtml):
    result = ''
    # print ans
    for answer in ans:
        if ifhtml:
            print(answer)
        else:
            if answer == u'\n':
                continue
            p = re.compile('<[^>]+>')
            result += p.sub("", answer.string).encode('utf8')
    return result


def ltptools(args):
    url_get_base = "http://api.ltp-cloud.com/analysis/"
    result = urllib.urlopen(url_get_base, urllib.urlencode(args))  # POST method
    content = result.read().strip()
    return content
