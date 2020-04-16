#!/usr/bin/env python
# -*- coding: utf-8 -*-
# модуль записи дампа "NNMclub.to" в БД sqlite3

import sqlite3, zlib,re
# import modbbcode

#CAT=[(8,'Темп, Архив'), (9,'NNM-Club'), (10,'Форум'),
#     (14,'Видео'), (16,'Музыка'), (17,'Игры'), (18,'Книги и Обучающие материалы'),
#     (21,'Программы, Операционные системы'), (23,'Документалистика, Телепередачи, Спорт, Юмор'), 
#     (24,'Аниме, Манга'), (26,'Всё для детей и родителей'), (27,'Сериалы'),
#     (28,'КПК и Мобильные устройства'), (29,'Клубные таланты'), (30,'Всё для Apple'),
#     (31,'Мультимедиа, Дизайн, Графика')]

def create_db(dirdb=''):    #Создание базы и заполнение таблицы категорий
    global DB,CAT
    DB=sqlite3.connect(dirdb + 'nnmclub.db3')
    cur=DB.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS "hdbk"
    ("numcode" smallint NOT NULL,
    "designation" varchar(100) NOT NULL,
    "up_code" smileint);

    CREATE TABLE IF NOT EXISTS "torrent"
    ("file_id" integer NOT NULL PRIMARY KEY,
    "hash_info" varchar(40) NOT NULL,
    "title" varchar(255) NOT NULL,
    "size_b" integer NOT NULL,
    "date_reg" varchar(20) NOT NULL,
    "code_id" smallint NOT NULL REFERENCES "hdbk" ("numcode"));

    CREATE INDEX IF NOT EXISTS "torrent_hdbk_id_b67937c0" ON "torrent" ("code_id");

    CREATE TABLE IF NOT EXISTS "vers"
    ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "vers" varchar(8) NOT NULL);
    """)

    cur.executescript("""DELETE FROM hdbk; DELETE FROM torrent; DELETE FROM vers;""")
#    cur.executemany('INSERT INTO hdbk(numcode,designation,up_code) VALUES (?, ?, 0);', CAT)
    dbc()
    cur.close()

def create_db_content(dirdb=''): # Создание доп. БД для хранения описаний раздач
    global DB1
    DB1=sqlite3.connect(dirdb + 'nnmcontent.db3')
    cur=DB1.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS "contents"
    ("tid" integer NOT NULL PRIMARY KEY,
    "cont" text NOT NULL);

    DELETE FROM contents;
    """)
    cur.close()
    
def dbc():
    try:
        DB.commit()
        DB1.commit()
    except:
        pass
    
def ins_forums(lists):
    for LLL in lists:
        try:
            DB.execute('INSERT INTO hdbk(numcode,designation,up_code) VALUES (?, ?, ?);', LLL)
        except:
            pass
    DB.commit()

def ins_vers(dt):
    DB.execute('INSERT INTO vers(vers) VALUES (?);', (dt,))
    DB.commit()

def ins_tor(id_podr,id_file,hash_info,title,size_b,date_reg):
    TOR=[(id_podr,id_file,hash_info,title,size_b,date_reg)]
    try:
        DB.execute('INSERT INTO torrent(code_id,file_id,hash_info,title,size_b,date_reg) SELECT ?,?,?,?,?,?;', (id_podr,id_file,hash_info,title,size_b,date_reg))
    except:
        dbc()

def ins_content(id_tor, cont):
    C = zlib.compress(cont.encode())
    try:
        DB1.execute('INSERT INTO contents(tid,cont) SELECT ?,?', (id_tor,C))
    except:
        dbc()

def sel_content(id_tor, dirdb=''):
    print('#'*80)
    DB1=sqlite3.connect(dirdb + 'nnmcontent.db3')
    cur=DB1.cursor()
    row=cur.execute('SELECT cont FROM contents WHERE tid=?;', (id_tor,))
    r=tuple(row)
    if len(r) != 0:
        S=zlib.decompress(r[0][0])
        S.decode('utf-8')
        print('========== Информация по %s ===========: \n %s ' % (id_tor, S.decode()))
    else:
        print('========== Нет информации по %s ========== \n' % (id_tor))
    
    cur.close()
    DB1.close()

    
    
def close_db():
    try:
        DB.execute('vacuum')
        DB.close()
        DB1.execute('vacuum')
        DB1.close()
    except:
        pass

if __name__ == '__main__':
    dirDB = 'C://DB/'
#    create_db('C://DB/')
#    ins_tor(2,3,'hash','title',12345,'2017.01.07 15:17:00')
#    ins_tor(2,4,'hash','title',12345,'2016.01.06 15:17:00')
#    create_db_content('C://DB/')
#    ins_content(3,'''Текст описания '''*100)
#    dbc()
    sel_content(239,dirDB)
#   DB.close()
    #test()

