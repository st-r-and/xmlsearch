#!/usr/bin/env python3
import os
import zipfile
import sqlite3
from datetime import date, time, datetime

class search:
    def __init__(self):
        self.name = 'xmlzip.db'
        self.conn = self.buildsql(self.name)
        self.count = 0

    def setquelle(quelle):
        pass

    def setziel(ziel):
        pass

    def setsearch(search):
        pass
        
    def listdir(self, dirname):
        files = os.listdir(dirname)
        return files

    def listzip(self, filename):
        zips = zipfile.ZipFile(filename, 'r')
        return zips.infolist()

    def listdirzip(self, dirname):
        files = self.listdir(dirname)
        for f in files:
            zipf = self.listzip(dirname + "/" + f)
            for z in zipf:
                list = []
                list.append(z.filename)
                list.append(z.date_time)
                list.append(z.file_size)
                list.append(f)
                self.safetosql(list)
        self.conn.commit()
        return self.count

    def exzip(self, quelle, ziel, datei)
        pass

    def findxml(self, search)
        pass

    
    def buildsql(self, name):
        conn = sqlite3.connect(name)
        conn.execute('CREATE TABLE if not exists ziplist(filename TEXT NOT NULL, xmlname TEXT NOT NULL, stamp DATE NOT NULL)')
        conn.execute('CREATE UNIQUE INDEX if not exists xml_unique ON ziplist(xmlname)')
        return conn
        

    def safetosql(self, data):
        d = date(data[1][0],data[1][1],data[1][2])
        t = time(data[1][3],data[1][4],data[1][5], 0)
        curs = self.conn.cursor()
        try:
            curs.execute('INSERT INTO ziplist(filename, xmlname, stamp) VALUES (?, ?, ?)',
                          (data[3], data[0], datetime.combine(d, t)))
        except sqlite3.IntegrityError:
            pass
        else:
            self.count +=1
            #print(data[0], 'schon da')
        #self.conn.commit()
        return 0


  
#dirname = "./ftp-sample"
dirname = "./ftp"
s = search()
c = s.listdirzip(dirname)
