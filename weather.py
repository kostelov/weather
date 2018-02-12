# -*- coding: utf-8 -*-

import json
import sqlite3
import time
import requests
import os


def parsejson(furl):
    elements = []
    base = []
    data = requests.get(furl).json()
    for item in data['list']:
        for datakey, datavalue in item.items():
            if datakey == 'weather':
                for k, v in datavalue[0].items():
                    if k == 'description':
                        elements.append(v)
            if datakey == 'main':
                for k, v in datavalue.items():
                    if k == 'temp':
                        elements.insert(1, v)
            if datakey == 'wind':
                if 'deg' not in datavalue:
                    elements.append(0)
                for k, v in datavalue.items():
                    if k == 'speed':
                        elements.insert(2, v)
                    if k == 'deg':
                        elements.insert(3, v)
            if datakey == 'dt' or datakey == 'id':
                elements.append(datavalue)
        base.append(tuple(elements))
        elements = []
    return base


def addrec(args):
    fullname = os.path.join(os.getcwd(), 'weather.db')
    with sqlite3.connect(fullname) as conn:
        curs = conn.cursor()
        curs.executemany('insert into metcast values(NULL, ?, ?, ?, ?, ?, ?)', args)


def receive():
    fullname = os.path.join(os.getcwd(), 'app.json')
    with open(fullname, 'r', encoding='utf-8') as jfile:
        appinf = json.load(jfile)
    townid = []
    fullname = os.path.join(os.getcwd(), 'weather.db')
    with sqlite3.connect(fullname) as con:
        cur = con.cursor()
        cur.execute('''
            create table if not exists metcast (
                id integer not null primary key autoincrement unique,
                wdescript text,
                temp real,
                wspeed real,
                wdeg real,
                dt integer,
                townid integer
            )
        ''')
        for row in cur.execute('select id from towns where country=\'{}\''.format(appinf['country'])):
            townid.append(str(*row))

    # '''
    #     openweather.org накладывает некоторые ограничения на free аккаунт:
    #     - не более 20 нас. пунктов в одном запросе
    #     - не более 60 запросов в минуту
    # '''

    if len(townid) % 20 != 0:
        n = len(townid) // 20 + 2
    else:
        n = len(townid) // 20
    count = 0
    for _ in range(n):
        if count != 42:
            url = 'http://api.openweathermap.org/data/2.5/group?id={}&lang=ru&units=metric&appid={}'\
                .format(','.join(townid[:20]), appinf['appid'])
            addrec(parsejson(url))
            count += 1
            del townid[:20]
        else:
            count = 0
            time.sleep(61)


if __name__ == '__main__':
    receive()
