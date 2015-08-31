#!/usr/bin/env python3
import os
import zipfile
import sqlite3

class search:
    def __init__(self):
        self.name = 'xmlzip.db'
        self.curs = self.buildsql(self.name)
        
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
        return self.count

    def buildsql(self, name):
        conn = sqlite3.connect(name)
        return conn.cursor()
        

    def safetosql(self, data):
        print(data[0], data[3])
        return 0


  
dirname = "./ftp-sample"
#dirname = "./ftp"
s = search()
print(s.listdirzip(dirname))
