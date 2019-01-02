# -*- coding:utf-8 -*-
#__author__: 'Baojian Jiang'
#__time__:'2019/1/2'
#analysis html

from bs4 import BeautifulSoup

class AnalysisHtml:

    def __init__(self, html):
        self.html = html

    def analysis_weather(self):
        # 0. use the download html file
        soup_html = BeautifulSoup(self.html, 'lxml')
        # print(soup.head)
        print(soup_html.title.get_text())#输出标题
        soup_div = soup_html.find('div', class_='tqtongji2')
        html_text = soup_div.get_text().split('\n\n')
        html_text = [i for i in html_text if i.strip() != ""]
        weather_list = []
        for i in range(1, len(html_text)):
            weather_list.append([x for x in html_text[i].split('\n') if x])
        return weather_list
