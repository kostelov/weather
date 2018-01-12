# -*- coding: utf-8 -*-

import json
import os
import sqlite3
# import datetime


def addrecord(filename):
    s = []
    k = []
    with open(filename, 'r', encoding='utf-8') as file:
        with sqlite3.connect('weather.db') as con:
            cur = con.cursor()
            cur.execute('''
                create table if not exists towns (
                    id integer primary key not null unique,
                    name text not null,
                    country text
                    )
            ''')
            for d in json.load(file):
                for value in d.values():
                    if type(value) != dict:
                        s.append(value)
                    else:
                        k.append(tuple(s))
                        s = []
                if len(k) == 50:
                    con.executemany('insert into towns values(?, ?, ?)', (tuple(k)))
                    k = []
            con.executemany('insert into towns values(?, ?, ?)', (tuple(k)))


fname = 'city.list.json'
addrecord(os.path.join(os.getcwd(), fname))
