# -*- coding: utf-8 -*-
# @Time    : 1/19/18 6:28 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : search.py
# @Software: PyCharm


import multiprocessing
import os
import threading
import time
from argparse import ArgumentParser
from datetime import datetime
from functools import partial
from multiprocessing import Queue, Event, Pipe

from alpfaceinterface.core.check_words import parse_false
from alpfaceinterface.core.chrome_search import run_browser
from alpfaceinterface.core.crawler.baiduzhidao import baidu_count_daemon
from alpfaceinterface.core.crawler.crawl import jieba_initialize, crawler_daemon

jieba_initialize()

# 包含题目和答案选项
get_wd = '题目'


# def parse_args():
#     parser = ArgumentParser(description="Million Hero Assistant")
#     parser.add_argument(
#         "-t", "--timeout",
#         type=int,
#         default=5,
#         help="default http request timeout"
#     )
#     return parser.parse_args()


def parse_question_and_answer(text_list):
    question = ""
    start = 0
    for i, keyword in enumerate(text_list):
        question += keyword
        if "?" in keyword:
            start = i + 1
            break
    real_question = question.split(".")[-1]

    for char, repl in [("以下", ""), ("下列", "")]:
        real_question = real_question.replace(char, repl, 1)

    question, true_flag = parse_false(real_question)
    return true_flag, real_question, question, text_list[start:]


def pre_process_question(keyword):
    """
    strip charactor and strip ?
    :param question:
    :return:
    """
    now = datetime.today()
    for char, repl in [("“", ""), ("”", ""), ("？", ""), ("《", ""), ("》", ""), ("我国", "中国"),
                       ("今天", "{0}年{1}月{2}日".format(now.year, now.month, now.day)),
                       ("今年", "{0}年".format(now.year)),
                       ("这个月", "{0}年{1}月".format(now.year, now.month))]:
        keyword = keyword.replace(char, repl)

    keyword = keyword.split(r"．")[-1]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    return keyword


# def main():
def search(wd):
    multiprocessing.freeze_support()
    # args = parse_args()
    timeout = 5#args.timeout

    stdout_queue = Queue(10)
    ## spaw baidu count
    baidu_queue = Queue(5)
    baidu_search_job = multiprocessing.Process(target=baidu_count_daemon,
                                               args=(baidu_queue, stdout_queue, timeout))
    baidu_search_job.daemon = True
    baidu_search_job.start()

    ## spaw crawler
    knowledge_queue = Queue(5)
    knowledge_craw_job = multiprocessing.Process(target=crawler_daemon,
                                                 args=(knowledge_queue, stdout_queue))
    knowledge_craw_job.daemon = True
    knowledge_craw_job.start()

    # 获取题目, 这是一个内层函数
    def __inner_job(keywords):
        start = time.time()
        if not keywords:
            keywords = get_wd  # 测试
        if not keywords:
            print("text not recognize")
            return

        true_flag, real_question, question, answers = parse_question_and_answer(keywords)

        if game_type == "UC答题":
            answers = map(lambda a: a.rsplit(":")[-1], answers)

        ### refresh question
        stdout_queue.put({
            "type": 0,
            "data": "{0}\n{1}".format(question, "\n".join(answers))
        })

        # notice baidu and craw
        baidu_queue.put((
            question, answers, true_flag
        ))
        knowledge_queue.put(question)

        end = time.time()
        stdout_queue.put({
            "type": 3,
            "data": "use {0} 秒".format(end - start)
        })

        time.time()

    # print("""
    #     请选择答题节目:
    #       1. 百万英雄
    #       2. 冲顶大会
    #       3. 芝士超人
    #       4. UC答题
    #     """)
    game_type = '1'  # input("输入节目序号: ")
    if game_type == "1":
        game_type = '百万英雄'
    elif game_type == "2":
        game_type = '冲顶大会'
    elif game_type == "3":
        game_type = "芝士超人"
    elif game_type == "4":
        game_type = "UC答题"
    else:
        game_type = '百万英雄'

    try:
        # 执行内层函数
        __inner_job(wd)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(str(e))

    # while True:
    #     # enter = input("按Enter键开始，按ESC键退出...")
    #     # if enter == chr(27):
    #     #     break
    #     try:
    #         #clear_screen()
    #         __inner_job()
    #     except Exception as e:
    #         import traceback
    #
    #         traceback.print_exc()
    #         print(str(e))

# if __name__ == "__main__":
#     multiprocessing.freeze_support()
#     main
