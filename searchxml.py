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
        self.edst = './error/'
        self.src = ''
        self.dst = ''
        self.search = ''

    def setsrc(self, src):
        if os.path.isdir(src):
            self.src = src
            return 1
        else:
            return 0

    def setdst(self, dst):
        if os.path.isdir(dst):
            self.dst = dst
            return 1
        else:
            return 0

    def setsearch(self, search):
        if os.path.isfile(search):
            self.search = search
            return 1
        else:
            return 0
        
    def getsrc(self):
        if self.src != '':
            return self.src
        else:
            return 0

    def getdst(self):
        if self.dst != '':
            return self.dst
        else:
            return 0

    def getsearch(self):
        if self.search != '':
            return self.search
        else:
            return 0
    
    def listdir(self):
        dirname = self.src
        files = os.listdir(dirname)
        return files

    def listzip(self, filename):
        zips = zipfile.ZipFile(filename, 'r')
        return zips.infolist()

    def listdirzip(self): #alle zip dateien im ordner
        dirname = self.src
        files = self.listdir()
        for f in files:
            if zipfile.is_zipfile(dirname + '/' + f):
                #print('alles ok')
                zipf = self.listzip(dirname + "/" + f)
                for z in zipf:                
                    list = [z.filename, z.date_time, z.file_size, f]
                    self.safetosql(list)
            else:
                print(f, 'hat einen Fehler')
                os.rename(dirname + '/' + f, self.edst + '/' + f)
        self.conn.commit()
        return self.count

    def exzip(self, quelle, ziel, datei):
        pass

    def findxml(self, search):
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
        except sqlite3.IntegrityError: #doppelte abfangen
            pass
        else:
            self.count +=1 # eingefügte zählen
            #print(data[0], 'schon da')
        #self.conn.commit()
        return 0


  
#dirname = "./ftp-sample"
dirname = "./ftp"
s = search()

#s.setsrc(dirname)

print(int(s.getsrc()))
#s.setsearch('id2.txt')
#print(s.getsearch())
#s.listdirzip()
