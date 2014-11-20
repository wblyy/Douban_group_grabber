# -*- coding: utf-8 -*-
import MySQLdb

class BaseDB(object):
    def __init__(self, database=None, user=None, passwd=None, host=None):
        self.database = database if database else 'mysql'
        self.user = user if user else 'root'
        self.passwd = passwd if passwd else '654321'
        #self.host = host if host else '114.243.222.166'#不需要输端口号
        self.host = host if host else 'soniegg.oicp.net'

    @property
    def db(self):
        return MySQLdb.connect(self.host, self.user, self.passwd, self.database, charset='utf8')

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def _execute(self, *args, **kwargs):
        conn = self.db
        cur = conn.cursor()
        cur.execute(*args, **kwargs)
        insert_id = cur.lastrowid
        conn.commit()
        return insert_id
        
    def _query_rows(self, *args):
        cur = self.db.cursor()
        cur.execute(*args)
        return cur.fetchall()

    def test_db(self):
        return self._query_rows('show tables')

class MydbV2(BaseDB):
    def __init__(self):
        BaseDB.__init__(self, database='douban_group')

    def insert_data(self, song, artist, language, producer, rights_owner):
        self._execute(r'insert ignore cavca_zpk(song, artist, language, producer, rights_owner) '
                      r'values (%s, %s, %s, %s, %s)', (song, artist, language, producer, rights_owner))
    def insert_douban_data(self, word, time, topicId, groupId):
        self._execute(r'insert ignore douban_group(word, time, topicId, groupId) '
                      r'values (%s, %s, %s, %s)', (word, time, topicId, groupId))    

    def insert_song(self, song, artist,album,top):
        self._execute('update meta_test set lyricist = '+lyricist+',composer='+composer+',arrangement='+arrangement+' where song='+song+' and artist='+artist+';'
                      , (song, artist, album,top))

    def insert_lyric(self, lyricist,composer,arrangement,song,artist):
		self._query_rows('update meta set lyricist = '+lyricist+',composer='+composer+',arrangement='+arrangement+' where song='+song+' and artist='+artist)
					  
    def get_id(self, song, artist):
        return self._query_rows('select id from meta where song=%s and artist=%s', (song, artist))

    def updat_song(self, lyricist, composer, arrangement, fxtime, song, artist):
        self._execute('update meta set lyricist=%s, composer=%s, arrangement=%s,album_release=%s where song=%s and artist=%s', (lyricist, composer, arrangement, fxtime,song, artist))
	
