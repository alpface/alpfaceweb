# -*- coding: utf-8 -*-
# @Time    : 1/18/18 7:14 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : text_process.py
# @Software: PyCharm

import jieba.posseg as pseg

'''
initialize jieba Segment
'''


def postag(text):
    words = pseg.cut(text)
    return words