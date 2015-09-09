#!/usr/bin/env python3
import os
import re
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

    def setsrc(self, src): # quellordner einstellen
        if os.path.isdir(src):
            self.src = src
            return 1
        else:
            return 0

    def setdst(self, dst): # zielordner einstellen -> für die xml files
        if os.path.isdir(dst):
            self.dst = dst
            return 1
        else:
            return 0

    def setsearch(self, search): # datei mit zu suchenden ID-codes
        if os.path.isfile(search):
            self.search = search
            return 1
        else:
            return 0
        
    def getsrc(self): # den quellordner zurückgeben
        if self.src != '':
            return self.src
        else:
            return 0

    def getdst(self): # den zielordner zurückgeben
        if self.dst != '':
            return self.dst
        else:
            return 0

    def getsearch(self): # die suchdatei zurückgeben
        if self.search != '':
            return self.search
        else:
            return 0
    
    def listdir(self): # die dateien aus dem quellordner auslesen
        dirname = self.src
        files = os.listdir(dirname)
        return files

    def listzip(self, filename): # zipdatei inhalt ausgeben
        zips = zipfile.ZipFile(filename, 'r')
        return zips.infolist()


    def listdirzip(self): #alle zip dateien im ordner
        dirname = self.src
        files = self.listdir()
        for f in files:
            if zipfile.is_zipfile(self.src + '/' + f):
                zipf = self.listzip(dirname + "/" + f)
                for z in zipf:                
                    list = [z.filename, z.date_time, z.file_size, f]
                    self.safetosql(list)
            else:
                print(f, 'hat einen Fehler')
                os.rename(dirname + '/' + f, self.edst + '/' + f)
        self.conn.commit()
        return self.count

    def listsearch(self):
        sfile = self.getsearch()
        if sfile:
            mode = 'r'
            fob = open(sfile, mode)
            liste = []
            for line in fob:
                if re.match("[0-9]{12}", line):
                    line = line.rstrip() + '.XML'
                    liste.append(line)
            fob.close()
            return liste
        else:
            return 0

    def exzip(self, xmlf, zipf):
        src = self.src
        dst = self.dst
        zf = zipfile.Zipfile(src + '/' + zipf, 'r')
        zf.extract(xmlf, dst)
        

    def findzip(self, xmlf):
        curs = self.conn.cursor()
        curs.execute('SELECT filename FROM ziplist WHERE xmlname = ? ORDER BY stamp DESC LIMIT 1', (xmlf,))
        #print(curs.fetchone())
        return curs.fetchone()
    
    def idtozip(self, idlist):
        if idlist:
            liste = []
            for oid in idlist:
                ozip = self.findzip(oid)
                if ozip != None:
                    liste.append(ozip[0])
                else:
                    liste.append(ozip)
            return liste
        else:
            return 0

    def buildsql(self, name):
        conn = sqlite3.connect(name)
        conn.execute('CREATE TABLE if not exists ziplist(filename TEXT NOT NULL, xmlname TEXT NOT NULL, stamp DATE NOT NULL)')
        conn.execute('CREATE UNIQUE INDEX if not exists xml_unique ON ziplist(xmlname, stamp)')
        # unique auf xmlname und stamp
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
#s.listdirzip()
s.setsearch("./IDs2.txt")
xmls = s.listsearch()
zips = s.idtozip(xmls)
print(len(xmls))
print(len(zips))
#print(int(s.getsrc()))
#s.setsearch('id2.txt')
#print(s.getsearch())

