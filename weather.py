# -*- coding: utf-8 -*-

import json
# import os
import sqlite3
import time
import requests

with open('app.json', 'r', encoding='utf-8') as jfile:
    appinf = json.load(jfile)

base = []
townid = []
elements = []
with sqlite3.connect('weather.db') as con:
    cur = con.cursor()
    # cur.execute('''
    #     create table if not exists metcast (
    #         id integer not null primary key autoincrement unique,
    #         wdescript text,
    #         temp real,
    #         wspeed real,
    #         wdeg real,
    #         dt integer,
    #         townid integer not null unique
    #     )
    # ''')
    for row in cur.execute('select id from towns where country=\'{}\''.format(appinf['country'])):
        townid.append(str(*row))

# '''
#     openweather.org накладывает некоторые ограничения на free аккаунт:
#     - не более 20 нас. пунктов в одном запросе
#     - не более 60 запросов в минуту
# '''

if len(townid) % 20 != 0:
    n = len(townid) // 20 + 1
else:
    n = len(townid) // 20
for i in range(n):
    if i != 42:
        url = 'http://api.openweathermap.org/data/2.5/group?id={}&lang=ru&units=metric&appid={}'\
            .format(','.join(townid[:20]), appinf['appid'])
        del townid[:20]
    else:
        time.sleep(61)
    # jfile = requests.get(url).json()

# with open('group.json', 'r', encoding='utf-8') as jfile:
# data = requests.get(url).json()
# for item in data['list']:
#     for datakey, datavalue in item.items():
#         if datakey == 'weather':
#             for k, v in datavalue[0].items():
#                 if k == 'description':
#                     elements.append(v)
#         if datakey == 'main' or datakey == 'wind':
#             for k, v in datavalue.items():
#                 if k == 'temp' or k == 'speed' or k == 'deg':
#                     elements.append(v)
#         if datakey == 'dt' or datakey == 'id':
#             elements.append(datavalue)
#     base.append(tuple(elements))
#     elements = []
# print(base)
