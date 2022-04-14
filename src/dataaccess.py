# -*- coding: utf-8 -*-

import common

import sqlite3
import os

class DataAccess():
    def __init__(self):
        db_path = os.path.join(common.assets_path, common.database_file)
        self.con = sqlite3.connect(db_path)

    def SuggestWord(self):
        sql = "SELECT [_id], [word], [stripword] FROM [dictionary] ORDER BY [stripword] ASC LIMIT %d" % common.data_size
        cur = self.con.execute(sql)
        result = []
        for row in cur:
            result.append({ "id": row[0], "word": row[1], "stripword": row[2] })
        return result

    def Word(self, search):
        result = []
        if search:
            search = search.replace("'", "''")
            search = search.replace("%", "")
            search = search.replace("_", "")
            
            if search.find("*") > -1 or search.find("?") > -1:
                search = search.replace("?", "_")
                search = search.replace("*", "%")
            else:
                search = search + "%"
            sql = """ SELECT [_id], [word], [stripword] FROM [dictionary] WHERE [stripword] LIKE '%s' ORDER BY [stripword] ASC """ % search
            cur = self.con.execute(sql)
            for row in cur:
                result.append({ "id": row[0], "word": row[1], "stripword": row[2] })
        return result

    def Definition(self, id):
        if id:
            sql = '''SELECT [_id], [word], [stripword], [title], [definition], 
            [keywords], [synonym], [filename], [picture], [sound] FROM [dictionary] 
            WHERE [_id] IS %d LIMIT 1 ''' % id

            cur = self.con.execute(sql)
            return cur.fetchone()

    def __del__(self):
        self.con.close()