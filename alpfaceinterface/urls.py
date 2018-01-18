# -*- coding: utf-8 -*-
# @Time    : 1/18/18 5:30 AM
# @Author  : alpface
# @Email   : xiaoyuan1314@me.com
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^answer/$', views.answer_options),
    url(r'^answertest/$', views.answer_test),
]