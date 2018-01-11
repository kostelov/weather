# -*- coding: utf-8 -*-

import json
import os
import sqlite3
import datetime


def pars(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        with sqlite3.connect('weather.db') as conn:
            for d in json.load(file):
                for key, value in d.items():
                    if type(value) != dict:
                        print(key, value)
                        sql = 'insert into towns ({}) values ({})'.format(key, value)
                        conn.execute(sql)


fname = 'city_list_test.json'
pars(os.path.join(os.getcwd(), fname))
