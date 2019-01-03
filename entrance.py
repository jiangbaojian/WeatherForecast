# -*- coding:utf-8 -*-
#__author__: 'Baojian Jiang'
#__time__:'2018/12/31'

import spyder
import time
import analysis
import pandas as pd

def save_txt(weather_info):
    with open('weather.txt', 'a') as fp:
        fp.write(weather_info)

def get_weather_info(html_text):
    html_text = html_text.split('\n\n')
    html_text = [i for i in html_text if i.strip() != ""]
    weather_list = []
    for i in range(1, len(html_text)):
        weather_list.append([x for x in html_text[i].split('\n') if x])
    return weather_list

if __name__ == '__main__':
    start_time = time.clock()
    time_list = []
    for year in range(2011, 2019):
        for month in range(1, 13):
            if month < 10:
                time_list.append(str(year) + '0' + str(month))
            else:
                time_list.append(str(year) + str(month))
    time_list = time_list[:-2]
    url_main = 'http://lishi.tianqi.com/tengzhou/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': 1,
        'Host': 'lishi.tianqi.com',
        'Upgrade-Insecure-Requests': 1,
        'Cookie': 'cityPy=zaozhuang; cityPy_expire=1547017400; UM_distinctid=1680d608af028a-0bb62dd0b72836-b781636-130980-1680d608af26d3; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1546412552,1546412658,1546412960,1546479069; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1546479069',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    data = []
    for each_time in time_list:
        url = url_main + each_time + '.html'
        # download = spyder.DownloaderSelf(user_agent=user_agent, cache=spyder.DiskCacheSelf(compress=False))
        # download = spyder.DownloaderSelf(user_agent=user_agent)
        download = spyder.DownloaderSelf(headers=headers, cache=spyder.DiskCacheSelf(compress=False))
        html = download(url=url).decode('gbk')
        print('开始解析' + each_time)
        weather = analysis.AnalysisHtml(html)
        weather_info = weather.analysis_weather()
        weather_info = pd.DataFrame(weather_info)
        data.append(weather_info)
    data = pd.DataFrame(data)
    data.to_csv('data.csv')
    end_time = time.clock()
    print('time:', end_time-start_time)
