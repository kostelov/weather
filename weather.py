# -*- coding: utf-8 -*-

import json
# import os
# import sqlite3
# import datetime
# import requests

# with open('app.id', 'r', encoding='utf-8') as file:
#     appid = file.read()
#
# town = 'Lutsk'
# with sqlite3.connect('weather.db') as con:
#     cur = con.cursor()
#     cur.execute('''
#         create table if not exists weather (
#             id integer not null primary key autoincrement unique,
#             townid integer not null unique,
#             wdescript text,
#             temp real,
#             wspeed real,
#             wdeg real,
#             dt integer
#         )
#     ''')
    # for row in cur.execute('select id, name from towns where name=\'{}\''.format(town)):
        # url = ('''http://api.openweathermap.org/data/2.5/weather?id={}&lang=ua&units=metric&appid={}
        #     '''.format(row[0], appid))
        # print(requests.get(url).json())
base = []
with open('weather.json', 'r', encoding='utf-8') as jfile:
    for datakey, datavalue in json.load(jfile).items():
        if datakey == 'weather':
            for k, v in datavalue[0].items():
                if k == 'description':
                    base.append(v)
        if datakey == 'main' or datakey == 'wind':
            for k, v in datavalue.items():
                if k == 'temp' or k == 'speed' or k == 'deg':
                    base.append(v)
        if datakey == 'dt':
            base.append(datavalue)
print(base)
