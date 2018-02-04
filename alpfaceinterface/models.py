# -*- coding: utf-8 -*-
# @Time    : 2/3/18 8:50 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : main.py
# @Software: PyCharm

from django.db import models


# class QuestionInfo(models.Model):
#     # 题目
#     question = models.CharField(max_length=1000)
#     # 答案选项 这里存储的是一个json字符串以\n\n为分隔符, 因为每个题目可能选项的数量不固定
#     ans_options = models.CharField(max_length=10000)
#     # 我们搜索到的推荐答案
#     recommended_option = models.CharField(max_length=2000)
#     # 搜索百度使用的url
#     baidu_url = models.CharField(max_length=10000)
#     # 搜索百度知道使用的url
#     baiduzhidao_url = models.CharField(max_length=10000)
#     # 开始时间
#     start_time = models.DateTimeField()
#     # 结束时间
#     end_time = models.DateTimeField()
#     # 结束时间
#
#     class Meta():
#         db_table = 'questioninfo'