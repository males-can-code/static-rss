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
                                                        "date_entered text            ,"
                                                        "feed         text            )")

        db.execute("create table if not exists groups (name        text            )")

        db.commit()
        db.close()


    def get_table(self, table):
    # Spits out the complete database into a list of dictionaries
        db = sqlite3.connect(self.db_path)
        rows = []
        for row in db.execute('select ROWID,* from %s order by ROWID'%table):
            rows.append(row)
        db.close()
        return rows


    def insert_row(self, table, row):
        # insert a group
        db = sqlite3.connect(self.db_path)
        values = []
        for key in row:
            values.append(row[key])
        query = 'INSERT INTO %s VALUES(%s)'%(table, ','.join(['?'] * len(row)))
        for k in row.keys():
            print(query)
            #db.execute("insert or ignore into %s(%s) values('%s')"%(table, k, str(row[k])))
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


    def get_feedlist(self, path):
        # Return a dictionary with name => url
        feedlist = []
        with open(path, 'r') as f:
            for line in f:
                feedlist.append(self.sanitize(line))
        return feedlist


    def get_timestamp(self):
        timestamp = strftime("%Y%m%d%H%M%S")
        return timestamp


    def check_file(self, filename):
        try:
            with open(filename) as f: pass
            return True
        except IOError as e:
            self.log.info('Failed to open file: %s'%filename)
            return False


    def check_dir(self, path):
        if not os.path.exists(path):
            self.log.info('dir doesn\'t exist, creating dir: %s'%path)
            try:
                os.makedirs(path)
                return True
            except IOError as e:
                self.log.error('Failed to create dir: %s'%path)
                sys.exit()
        else:
            return True


    def write_to_file(self, path, data):
        try:
            f = open(path, 'w')
            f.write(data)
            f.close()
        except IOError:
            self.log.error('Failed to write to file: %s'%path)


    def parse_feed(self, feed):
        self.log.info('Parsing: %s'%feed)
        try:
            feed = feedparser.parse(feed)
            return feed
        except:
            self.log.error('Failed to parse feed: %s'%feed)
            return False


    def parse_feedlist(self, feedlist):
        # parse the feedlist and write new entries to file in feedhash/unread/titlehash
        feeds = {}
        for feed_url in feedlist:
            feed_parsed = self.parse_feed(feed_url)
            if feed_parsed:

                feed_url_hashed = self.hash(feed_url)
                feed_path = self.feeds_path + '/' + feed_url_hashed
                feed_read_path = self.feeds_path + '/' + feed_url_hashed + '/read'
                feed_unread_path = self.feeds_path + '/' + feed_url_hashed + '/unread'

                self.check_dir(feed_path)
                self.check_dir(feed_read_path)
                self.check_dir(feed_unread_path)

                items_read = self.get_dir_contents(feed_read_path)
                items_unread = self.get_dir_contents(feed_unread_path)
                items_read_hashes = []
                items_unread_hashes = []
                for item in items_read:
                    x,item_read_hash = item.split('|')
                    item_read_hash = self.sanitize(item_read_hash)
                    items_read_hashes.append(item_read_hash)
                for item in items_unread:
                    x,item_unread_hash = item.split('|')
                    item_unread_hash = self.sanitize(item_unread_hash)
                    items_unread_hashes.append(item_unread_hash)

                for item in feed_parsed.entries:
                    item_title_hashed = self.hash(item['title'])
                    if item_title_hashed not in items_unread_hashes and item_title_hashed not in items_read_hashes:
                        self.log.debug('New title: ' + item_title_hashed)
                        self.write_to_file(self.feeds_path + '/' + feed_url_hashed + '/unread/' + self.get_timestamp() + '|' + item_title_hashed, item['summary'])

                feeds[feed_url_hashed] = feed_parsed

        return feeds


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


    def get_hash(self, data):
        data = self.sanitize(data)
        data = self.encode(data)
        hashed = hashlib.sha224(data).hexdigest()
        return hashed


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


            
        


    def run(self):
        #self.check_dir(self.feeds_path)
        #self.check_dir(self.template_path)
        #if not self.check_file(self.feedlist_path):
        #    self.log.error('No feedlist found at: %s... Quitting'%self.feedlist_path)

        #feedlist = self.get_feedlist(self.feedlist_path)
        #self.feeds = self.parse_feedlist(feedlist)
        #html = GenerateHTML(self.template_path, self.feeds_path, self.HTML_path)
        #html.run()
        self.create_tables()
        self.add_feed('http://iloveubuntu.net/rss.xml')
        self.get_table('feeds')


app = RSS()
app.run()
