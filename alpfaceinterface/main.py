# -*- coding: utf-8 -*-
# @Time    : 2/3/18 8:50 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : main.py
# @Software: PyCharm

from datetime import datetime
from alpfaceinterface.search import search


negate_word = ['没有', '不是', '不会', '不包括', '不属于', '无关', '不可能', '错误']
auxiliary_word = ['下列', '以下', '哪个', '?']

def main(ques):
    start = datetime.now()  # 记录开始时间
    if ques is None:
        ques = '"孟姜女是哪个朝代的人?\n\n唐代\n\n秦朝\n\n宋代"'
    question, option_arr, is_negative = parse_question(ques)
    print('搜索的题目是：{} '.format(question))
    print('选项为：{} '.format(option_arr))
    if question is None or question == '':
        print('未获取到问题')
        return '未获取到问题', -1
    best_answer, best_index = search(question, option_arr, is_negative)  # 搜索结果

    if best_answer is None:
        print('\n没有答案')
        best_index = -1
    else:
        print('推荐答案是： \033[1;31m{}\033[0m'.format(best_answer))
    run_time = (datetime.now() - start).seconds
    print('本次运行时间为：{}秒'.format(run_time))
    return best_answer, best_index




def parse_question(text):
    '''解析问题和答案选项字符串'''
    question, option_arr = get_question(text)
    question, is_negative = analyze_question(question)
    return question, option_arr, is_negative

def get_question(text):
    options = ''
    option_arr = []
    question = ''
    text_arr = text.split('\n\n')
    if len(text_arr) > 0:
        question = text_arr[0]
        # question = question.strip()[2:]
        if len(text_arr) > 1:
            for opt in text_arr[1:]:
                options += '\n' + opt
    if options is not None:
        option_arr_o = options.split('\n')
        for op in option_arr_o:
            if op != '' and not op.isspace():
                if op.startswith('《'):
                    op = op[1:]
                if op.endswith('》'):
                    op = op[:-1]
                option_arr.append(op)
                print(op)
    return question, option_arr


# 分析题目，去掉否定词及无关词，得到题目所求答案正反
def analyze_question(question):
    extra_word = negate_word + auxiliary_word
    is_negate = False
    for ele in extra_word:
        if ele in negate_word and ele in question:
            is_negate = True
        if ele in question:
            question = question.replace(ele, '')
    return question, is_negate
