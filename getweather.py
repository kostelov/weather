# -*- coding: utf-8 -*-

import sys
import sqlite3
from datetime import datetime


def hlp(*args):
    print('''
        Получить архив погоды на дату:
        python getweather.py get <Населенный_пункт> <дд.мм.гггг>
    ''')


def weatherget(townname, udt):
    wdeg = ''
    udt = int(datetime.strptime(udt, '%d.%m.%Y').timestamp())
    with sqlite3.connect('weather.db') as conn:
        curs = conn.cursor()
        for townid in curs.execute('SELECT id FROM towns WHERE country=\'UA\' '
                                   'AND name=\'{}\' LIMIT 1'.format(townname.capitalize())):
            for row in curs.execute('SELECT wdescript, temp, wspeed, wdeg, dt '
                                    'FROM metcast WHERE townid=\'{}\' AND '
                                    'dt>=\'{}\' AND dt<\'{}\''.format(*townid, udt, udt + 86400)):

                # к дате указаной пользователем прибавляем 86400 с = 24 ч = 1 сутки чтобы получить
                # погоду в пределах суток

                if 0 <= row[3] < 22.5 or 337.5 <= row[3] <= 360:
                    wdeg = 'С'
                elif 22.5 <= row[3] < 67.5:
                    wdeg = 'С-В'
                elif 67.5 <= row[3] < 112.5:
                    wdeg = 'В'
                elif 112.5 <= row[3] < 157.5:
                    wdeg = 'Ю-В'
                elif 157.5 <= row[3] < 202.5:
                    wdeg = 'Ю'
                elif 202.5 <= row[3] < 247.5:
                    wdeg = 'Ю-З'
                elif 247.5 <= row[3] < 292.5:
                    wdeg = 'З'
                elif 292.5 <= row[3] < 337.5:
                    wdeg = 'С-З'
                print('''
                    Дата и время: {}
                    Метеоусловия: {}
                    Температура: {} °C
                    Скорость ветра: {} м/с
                    Направление ветра: {}
                '''.format(datetime.fromtimestamp(row[4]).strftime('%d.%m.%Y %H:%M'), row[0], row[1], row[2], wdeg))


if __name__ == '__main__':
    do = {
        "help": hlp,
        "get": weatherget
    }
    try:
        userdate = sys.argv[3]
    except IndexError:
        userdate = None

    try:
        town = sys.argv[2]
    except IndexError:
        town = None

    try:
        key = sys.argv[1]
    except IndexError:
        key = None

    if do.get(key):
        do[key](town, userdate)
    else:
        print('Неверный ключ или не указаны параметры')
