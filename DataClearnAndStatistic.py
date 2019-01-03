# -*- coding:utf-8 -*-
#__author__: 'Baojian Jiang'
#__time__:'2019/1/3'

import pandas as pd

def generate_ultimate_csv():
    '''生成最终的data csv文件，简单去掉无效的数据并进行分列'''
    data_origin = pd.read_csv('data.csv')
    # print(data)
    header = ['id', 'date', 'max_temperature', 'min_temperature', 'weather', 'wind_direction', 'wind_power']
    # print(data.columns.values.tolist())
    data = []
    for i in data_origin.values:
        data.append([j for j in i[0].split(' ') if j != ''])
    data = pd.DataFrame(data, columns=header)
    data = data.drop(['id'], axis=1)  # 删除第一列
    # drop_index = data.loc[data['date'] == '0']
    drop_index = data[data.date == '0'].index.tolist()  # 获取错误行的索引index
    data = data.drop(drop_index, axis=0)  # 删除错误行
    data.to_csv('ultimate_data.csv')

if __name__ == '__main__':
    print('1, 生成CSV文件')
    # generate_ultimate_csv()
    print('2, 读取ultimate_csv文件')
    data = pd.read_csv('ultimate_data.csv')
    data[['max_temperature', 'min_temperature']] = data[['max_temperature', 'min_temperature']].astype(int)#改变数据类型
    max_tempe = data['max_temperature'].max()
    print(max_tempe)
    min_temp = data['min_temperature'].min()
    print(min_temp)
    mean_temp = data['max_temperature'].mean()
    print(mean_temp)