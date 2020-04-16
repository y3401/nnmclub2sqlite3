#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os, os.path
import sys
import NNM_sql3 as lite
import time

D = {}
List=[]

time_begin = 0  
time_end = 0    


def ReadFile(infile):      
    k = 0
    n = 0
    D.clear()
    
    with open(infile,encoding='utf-8') as lines:
        try:
            while True:
                line = next(lines)
                if (line.rstrip('\n') == '---NEXT---' and n > 8):
                    k += 1
                    parsline()
                    if k%1000 == 0:
                        lite.dbc()
                        print(k) 
                    D.clear()
                    n = 1
                else:
                    D[n] = line.rstrip('\n')
                    n += 1
        except StopIteration:
            if n > 8:
                k += 1
                parsline()
    print(k)
    lite.dbc()

def parsline():      #разбор блока данных и запись в базу
    tid = ''
    reg_date = ''
    b_size = '0'
    title = ''
    magnet = ''
    forum_id = ''
    forum = ''
    contents = ''
    magnet = D.get(1)
    tid = D.get(2).split('=')[1]
    title = D.get(3)
    forum_id = (D.get(4).split(' // ')[0]).split(':')[1]
    if D.get(6) != '': b_size = D.get(6)
    reg_date = D.get(7)
    contents = D.get(9)
    lite.ins_tor(forum_id,tid,magnet,title,b_size,reg_date)
    if max(D.keys()) >= 9:
        for key in range(max(D.keys())):
            if key >= 9:
                contents=contents + str(D.get(key)).rstrip('\n')
    lite.ins_content(tid,contents)


def load_forums3(infile):       # Загрузка справочников (vers 3)
    for line in open(infile, encoding = 'utf-8'):
        forum = line.split(sep=';')[0]
        name_forum=line.split(sep=';')[1]
        category = line.split(sep=';')[2]
        List.append((int(forum),str(name_forum),int(category)))


# START PROG ->
if __name__ == '__main__':
    for f in os.listdir('.'):
        if f[:4] == 'nnm-':
            backup = f
            #break
    	
    period = backup.split("-")[1][:8]
    dirDB = 'C://DB/'
    print('Обрабатываемый файл: ' + backup)
    time_begin=time.time()
    load_forums3('spr.csv')
#    load_forums3('podr.csv')
    print('Словари загружены')

    if not os.path.exists(dirDB):
        os.mkdir(dirDB)
    lite.create_db(dirDB)                                
    lite.create_db_content(dirDB+'/')
    lite.ins_vers(period)
    lite.ins_forums(List)
    ReadFile(backup)
    lite.close_db()
    time_end=time.time()
    tsec=time_end-time_begin
    stsec=(str(tsec)).split('.')
    tsec=int(stsec[0])
    seconds=0
    minutes=0
    hours=0
    n=0
    seconds=tsec % 60
    minutes=(tsec//60) % 60
    hours=(tsec//3600) % 24
    print('Готово!')
    print('Затраченное время - %s:%s:%s' % (str(hours),('0'+str(minutes))[-2:],('0'+str(seconds))[-2:]))


