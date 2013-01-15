#!/usr/bin/python3

import os,sys
import feedparser
import hashlib
from log import Log
from color import Color
from time import strftime
from string import Template
import sqlite3


class GenerateHTML(object):
    def get_files(self, path):
        for path,dirs,files in os.walk(path):
            return files


    def check_dir(self, directory):
        if not os.path.exists(directory):
            self.log.info('dir doesn\'t exist, creating dir: %s'%directory)
            try:
                os.makedirs(directory)
                return True
            except IOError as e:
                self.log.error('Failed to create dir: %s'%directory)
                sys.exit()
        else:
            self.log.info('path exists: %s'%directory)
            return True


    def check_file(self, filename):
        try:
            with open(filename) as f: pass
            return True
        except IOError as e:
            self.log.info('Failed to open file: %s'%filename)
            return False
        

    def get_file(self, filename):
        contents = []
        if self.check_file(filename):
            try:
                f = open(filename, 'r')
            except IOError as e:
                self.log.info('Failed to open file: %s'%filename)
                return False

            for line in f:
                contents.append(self.sanitize(line))
            f.close()
            return contents
        else:
            return False
            

    def write_to_file(self, path, templates):
        write_data = ''
        try:
            f = open(path, 'w')
        except IOError:
            self.log.error('Failed to write to file: %s'%path)

        for template in templates:
            for x in template:
                write_data = write_data + x
        f.write(write_data)
        f.close()


    def parse_feed_template(self, template_path, entry):
        data = self.get_file(template_path)
        filled_template = []

        if data:
            for line in data:
                replaced = False
                for key in entry.keys():
                    if '$' + key in line:
                        line = Template(line).substitute({key:entry[key]})
                filled_template.append(line)
        return filled_template


    def generate_HTML(self):
        templates = []
        feeds = self.get_table('feeds')
        for feed in feeds:
            entries = self.get_entries_by_hash('entries', str(self.get_hash(feed['feed_url']))) 
            for entry in entries:
                filled_template = self.parse_feed_template(self.feed_template_path, entry)
                templates.append(filled_template)
            self.write_to_file('/home/eco/bin/apps/rss/html/index.html', templates)





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
                                                        "entry_url    text            ,"
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


    def get_entries_by_hash(self, table, feed_hash):
        db = sqlite3.connect(self.db_path)
        rows = []
        cols = []
        table_export = []

        for row in db.execute('select * from %s where "feed_hash" is "%s"'%(table, feed_hash)):
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
        try:
            db.execute(query,values)
            db.commit()
            db.close()
        except:
            self.log.error('Failed to insert row')
            db.close()


    def check_in_table(self, table, value):
        db = sqlite3.connect(self.db_path)
        for data in db.execute('select * from %s where hash = ?'%table, (value,)):
            if data:
                db.close()
                return True
        db.close()
        return False
        


class RSS(Database, GenerateHTML):
    def __init__(self):
        self.db_path = '/home/eco/bin/apps/rss/rss.db'
        self.HTML_path = '/home/eco/bin/apps/rss/html'
        self.feed_template_path = '/home/eco/bin/apps/rss/templates/feed.html'
        self.feeds = {}     # Contains feeds: key: hashed url, value: parsed feed object
        self.log = Log()
        self.color = Color()


    def get_timestamp(self):
        timestamp = strftime("%Y%m%d%H%M%S")
        return timestamp


    def get_hash(self, data):
        data = self.sanitize(data)
        data = self.encode(data)
        hashed = hashlib.sha224(data).hexdigest()
        return hashed


    def parse_feed(self, url):
        self.log.info('Parsing: %s'%url)
        try:
            parsed_feed = feedparser.parse(url)
            return parsed_feed
        except:
            self.log.error('Failed to parse feed: %s'%url)
            return false


    def parse_feeds(self):
        feeds = self.get_table('feeds')
        for feed in feeds:
            parsed_feed = self.parse_feed(feed['feed_url'])
            if parsed_feed:
                for entry in parsed_feed.entries:
                    if not self.check_in_table('entries',str(self.get_hash(entry['title']))):
                        self.add_entry(entry, feed['feed_url'])


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
        self.log.info('Adding feed: %s'%url)
        feed_insert = {}
        feed = self.parse_feed(url)
        if feed:
            feed_insert['hash'] = str(self.get_hash(url))
            feed_insert['title'] = str(feed.feed['title'])
            feed_insert['date_entered'] = str(self.get_timestamp())
            feed_insert['feed_url'] = str(url)
            feed_insert['icon_url'] = 'None'
            feed_insert['last_updated'] = 'None'
            feed_insert['group_id'] = '0'

            self.insert_row('feeds', feed_insert)


    def add_entry(self, entry, url):
        self.log.info('Inserting new entry: %s'%entry['title'])
        entry_insert = {}
        entry_insert['hash'] = str(self.get_hash(entry['title']))
        entry_insert['content'] = str(entry['summary'])
        entry_insert['entry_url'] = str(entry['link'])
        entry_insert['read'] = 'False'
        entry_insert['title'] = str(entry['title'])
        entry_insert['date_entered'] = str(self.get_timestamp())
        entry_insert['feed_hash'] = str(self.get_hash(url))

        self.insert_row('entries', entry_insert)


    def insert_test_feeds(self):
        urls = ['http://inconsolation.wordpress.com/feed/', 'http://iloveubuntu.net/rss.xml', 'http://feeds.bbci.co.uk/news/rss.xml']
        for url in urls:
            if not self.check_in_table('feeds',str(self.get_hash(url))):
                self.add_feed(url)


    def run(self):
        self.create_tables()
        self.insert_test_feeds()
        self.parse_feeds()
        self.generate_HTML()



app = RSS()
app.run()
