#!/usr/bin/python3

import os,sys
import feedparser
import hashlib
from log import Log
from color import Color
from time import strftime
import sqlite3


class GenerateHTML(object):
    def __init__(self, templ_path, src_path, dest_path):
        self.templ_path = templ_path
        self.src_path = src_path
        self.dest_path = dest_path


    def get_files(self, path):
        for path,dirs,files in os.walk(path):
            return files


    def get_dirs(self, path):
        for path,dirs,files in os.walk(path):
            return dirs


    def read_file(self, path):
        file_content = []
        with open(path, 'r') as f:
            for line in f:
                file_content.append(line)
        return file_content


    def generate_HTML(self):
        pass


    def run(self):
        feed_dirs = self.get_dirs(self.src_path)
        for feed_dir in feed_dirs:
            
            for item in self.get_files(self.src_path + '/' + feed_dir + '/read'):
                content = self.read_file(self.src_path + '/' + feed_dir + '/read/' + item)
            for item in self.get_files(self.src_path + '/' + feed_dir + '/unread'):
                content = self.read_file(self.src_path + '/' + feed_dir + '/unread/' + item)

            # now write stuff with help from template files to html
            # next would probably be the php file for marking everything as read
        

class Database(object):
    def create_tables(self):
        db = sqlite3.connect(self.db_path)
        db.execute("create table if not exists feeds (hash          text    unique  ,"
                                                     "title         text            ,"
                                                     "date_entered  text            ,"
                                                     "feed_url      text            ,"
                                                     "icon_url      text            ,"
                                                     "last_updated  text            ,"
                                                     "group_id      text            )")

        db.execute("create table if not exists entries (hash          text    unique  ,"
                                                        "content      text            ,"
                                                        "title        text            ,"
                                                        "read         text            ,"
                                                        "date_entered text            ,"
                                                        "feed_hash    text            )")

        db.execute("create table if not exists groups (name        text            )")

        db.commit()
        db.close()


    def get_table(self, table):
    # Spits out the complete table into a list of dictionaries
        db = sqlite3.connect(self.db_path)
        rows = []
        cols = []
        table_export = []

        for row in db.execute('select * from %s order by ROWID'%table):
            rows.append(row)

        for row in db.execute('PRAGMA table_info(%s)'%table):
            cols.append(row[1])

        for row in rows:
            row_export = {}
            for x in range(1,len(cols)):
                row_export[cols[x]] = row[x]
            table_export.append(row_export)

        db.close()
        return table_export


    def insert_row(self, table, row):
        db = sqlite3.connect(self.db_path)
        values = []
        for key in row:
            values.append(row[key])
        keys = ','.join(row.keys())
        query = 'INSERT INTO %s(%s) VALUES(%s)'%(table, keys, ','.join(['?'] * len(row)))
        db.execute(query,values)
        db.commit()
        self.log.debug('Row inserted')
        db.close()
        



class RSS(Database):
    def __init__(self):
        self.db_path = '/home/eco/bin/apps/rss/rss.db'
        self.HTML_path = '/home/eco/bin/apps/rss/html'
        self.feedlist_path = '/home/eco/bin/apps/rss/feedslist'
        self.feeds_path = '/home/eco/bin/apps/rss/feeds'
        self.template_path = '/home/eco/bin/apps/rss/templates/feed'
        self.feeds = {}     # Contains feeds: key: hashed url, value: parsed feed object
        self.log = Log()
        self.color = Color()

        # Map fields in tables to index in list so it's easier to change the order
        self.group_id_field               = 0
        self.group_title_field            = 1

        self.entries_hash_field           = 0
        self.entries_content_field        = 1
        self.entries_date_entered_field   = 2
        self.entries_feed_field           = 3

        self.feeds_hash_field             = 0
        self.feeds_title_field            = 1
        self.feeds_date_entered_field     = 2
        self.feeds_feed_url_field         = 3
        self.feeds_last_updated_field     = 4
        self.feeds_group_id_field         = 5


    def get_timestamp(self):
        timestamp = strftime("%Y%m%d%H%M%S")
        return timestamp


    def get_hash(self, data):
        data = self.sanitize(data)
        data = self.encode(data)
        hashed = hashlib.sha224(data).hexdigest()
        return hashed


    def parse_feed(self, feed):
        self.log.info('Parsing: %s'%feed)
        try:
            feed = feedparser.parse(feed)
            return feed
        except:
            self.log.error('Failed to parse feed: %s'%feed)
            return False


    def sanitize(self, var):
        # Strip file from blanks and newlines
        var = var.strip()
        return var


    def decode(self, data):
        data = data.decode('utf-8')
        return data


    def encode(self, data):
        data = data.encode('utf-8')
        return data


    def add_feed(self, url):
        feed = self.parse_feed(url)
        feed_insert = {}
        if feed:
            feed_insert['hash'] = str(self.get_hash(url))
            feed_insert['title'] = str(feed.feed['title'])
            feed_insert['date_entered'] = str(self.get_timestamp())
            feed_insert['feed_url'] = str(url)
            feed_insert['icon_url'] = str('None')
            feed_insert['last_updated'] = str('None')
            feed_insert['group_id'] = str(0)

            print(feed_insert)
            self.insert_row('feeds', feed_insert)


    def add_entry(self, entry, url):
        entry_insert = {}
        entry_insert['hash'] = str(self.get_hash(entry['published'] + entry['title']))
        entry_insert['content'] = str(entry['summary'])
        entry_insert['read'] = 'False'
        entry_insert['title'] = str(entry['title'])
        entry_insert['date_entered'] = str(self.get_timestamp())
        entry_insert['feed_hash'] = str(self.get_hash(url))

        self.insert_row('entries', entry_insert)


    def run(self):
        self.create_tables()
        self.add_feed('http://inconsolation.wordpress.com/feed/')
        self.add_feed('http://iloveubuntu.net/rss.xml')


        feeds = self.get_table('feeds')
        for feed in feeds:
            parsed_feed = self.parse_feed(feed['feed_url'])
            for entry in parsed_feed.entries:
                self.add_entry(entry, feed['feed_url'])

        entries = self.get_table('entries')
        for entry in entries:
            print('>>>',entry['title'])
app = RSS()
app.run()
