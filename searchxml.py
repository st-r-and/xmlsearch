#!/usr/bin/env python3
import os
import zipfile
import sqlite3
from datetime import date, time, datetime

class search:
    def __init__(self):
        self.name = 'xmlzip.db'
        self.conn = self.buildsql(self.name)
        
    def listdir(self, dirname):
        files = os.listdir(dirname)
        return files

    def listzip(self, filename):
        zips = zipfile.ZipFile(filename, 'r')
        return zips.infolist()

    def listdirzip(self, dirname):
        self.count = 0
        files = self.listdir(dirname)
        for f in files:
            zipf = self.listzip(dirname + "/" + f)
            for z in zipf:
                # timestemp = gettimestamp()
                list = []
                list.append(z.filename)
                list.append(z.date_time)
                list.append(z.file_size)
                list.append(f)
                # list.append(timestamp)
                # safetosql(list)
                # print(z.filename, z.date_time, z.file_size, f, timestamp)
                self.safetosql(list)
                self.count +=1
        self.conn.commit()
        return self.count

    def buildsql(self, name):
        conn = sqlite3.connect(name)
        conn.execute('CREATE TABLE if not exists ziplist(filename TEXT, xmlname TEXT, stamp DATE)')
        return conn
        

    def safetosql(self, data):
        d = date(data[1][0],data[1][1],data[1][2])
        t = time(data[1][3],data[1][4],data[1][5], 0)
        curs = self.conn.cursor()
        curs.execute('INSERT INTO ziplist(filename, xmlname, stamp) VALUES (?, ?, ?)',
                          (data[3], data[0], datetime.combine(d, t)))
        #self.conn.commit()
        return 0


  
#dirname = "./ftp-sample"
dirname = "./ftp"
s = search()
print(s.listdirzip(dirname))
