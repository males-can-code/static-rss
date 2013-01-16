#!/usr/bin/python3

import os,sys
import feedparser
import hashlib
import sqlite3
import shutil
from log import Log
from color import Color
from time import strftime
from string import Template


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
            

    def write_to_file(self, path, data):
        try:
            with open(path, 'w') as f:
                f.write(data)
        except IOError:
            self.log.error('Failed to write to file: %s'%path)


    def parse_template(self, template_path, data):
    # Parse a template file and return a list
        filled_template = ''
        template = self.get_file(template_path)

        if template:
            for line in template:
                for key in data.keys():
                    if '$' + key in line:
                        line = Template(line).safe_substitute({key:data[key]})
                filled_template = filled_template + line + '\n'

        return filled_template


    def generate_feed_urls(self, feeds):
        filled_urls_template = ''
        feed_url = {}
        c = 0
        
        for feed in feeds:
            # Count unread entries per feed
            entries = self.get_entries_by_hash('entries', str(self.get_hash(feed['feed_url']))) 
            for entry in entries:
                if entry['read'] == 'False':
                    c = c + 1

            feed_url['title'] = feed['title'] 
            feed_url['feed_url'] = self.export_html_path + '/feeds/' + feed['hash'] + '/feed.html'
            feed_url['counter'] = c

            # Parse template
            filled_url_template = self.parse_template(self.feed_urls_template_path, feed_url)
            filled_urls_template = filled_urls_template + filled_url_template + '\n'
        return filled_urls_template


    def generate_entries(self, feed):
        filled_entries_template = ''
        entries = self.get_entries_by_hash('entries', str(self.get_hash(feed['feed_url']))) 
        for entry in entries:
            # Use different template for read/unread entries
            if entry['read'] == 'True':
                filled_entry_template = self.parse_template(self.read_entry_template_path, entry)
            elif entry['read'] == 'False':
                filled_entry_template = self.parse_template(self.unread_entry_template_path, entry)

            filled_entries_template = filled_entries_template + filled_entry_template + '\n'

        return filled_entries_template


    def generate_HTML(self):
        shutil.rmtree(self.export_html_path)
        self.check_dir(self.export_html_path)
        self.check_dir(self.export_html_path + '/feeds')

        feeds = self.get_table('feeds')

        feed_template = {}
        feed_template['css'] = self.css_path
        feed_template['feed_urls'] = self.generate_feed_urls(feeds)

        for feed in feeds:
            feed_template['content'] = self.generate_entries(feed)
            feed_template['title'] = feed['title']
            filled_feed_template = self.parse_template(self.feed_template_path, feed_template)

            self.check_dir(self.export_html_path + '/feeds/' + feed['hash'])
            self.write_to_file(self.export_html_path + '/feeds/' + feed['hash'] + '/feed.html', filled_feed_template)

            if feed == feeds[0]:
                self.write_to_file(self.export_html_path + '/index.html', filled_feed_template)



class Database(object):
    def create_tables(self): 
        db = sqlite3.connect( self.db_path)
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
            for x in range(0,len(cols)):
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
        self.export_html_path = '/home/eco/bin/apps/rss/html'
        self.read_entry_template_path = '/home/eco/bin/apps/rss/templates/read_entry.html'
        self.unread_entry_template_path = '/home/eco/bin/apps/rss/templates/unread_entry.html'
        self.feed_template_path = '/home/eco/bin/apps/rss/templates/feed.html'
        self.feed_urls_template_path = '/home/eco/bin/apps/rss/templates/feed_urls.html'
        self.css_path = '/home/eco/bin/apps/rss/css/stylesheet.css'
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
