# -*- coding: utf-8 -*-

# import json
# import os
import sqlite3
# import datetime
import requests

with open('app.id', 'r', encoding='utf-8') as file:
    app_id = file.read().strip()

base = []
townid = []
elements = []
country = 'UA'
with sqlite3.connect('weather.db') as con:
    cur = con.cursor()
    cur.execute('''
        create table if not exists weather (
            id integer not null primary key autoincrement unique,
            wdescript text,
            temp real,
            wspeed real,
            wdeg real,
            dt integer,
            townid integer not null unique
        )
    ''')
    for row in cur.execute('select id from towns where country=\'{}\' limit 20'.format(country)):
        townid.append(str(*row))
    url = 'http://api.openweathermap.org/data/2.5/group?id={}&lang=ru&units=metric&appid={}'\
        .format(','.join(townid), app_id)
    # jfile = requests.get(url).json()

# with open('group.json', 'r', encoding='utf-8') as jfile:
data = requests.get(url).json()
for item in data['list']:
    for datakey, datavalue in item.items():
        if datakey == 'weather':
            for k, v in datavalue[0].items():
                if k == 'description':
                    elements.append(v)
        if datakey == 'main' or datakey == 'wind':
            for k, v in datavalue.items():
                if k == 'temp' or k == 'speed' or k == 'deg':
                    elements.append(v)
        if datakey == 'dt' or datakey == 'id':
            elements.append(datavalue)
    base.append(tuple(elements))
    elements = []
print(base)
