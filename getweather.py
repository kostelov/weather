# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime


def gettownid(townname):
    with sqlite3.connect('weather.db') as conn:
        curs = conn.cursor()
        for row in curs.execute('select id from towns where country=\'UA\' and name=\'{}\' limit 1'.format(townname)):
            print(row)


if __name__ == '__main__':
    gettownid(input('город: ').capitalize())
    udt = int(datetime.strptime(input('дата: '),'%d.%m.%Y').timestamp())
    dt = int(datetime.utcnow().timestamp())
    delta = datetime.fromtimestamp(dt) - datetime.fromtimestamp(udt)
    print(dt, udt, delta.days)
    print(datetime.fromtimestamp(1516285745).strftime('%d.%m.%Y'))
