#!/usr/bin/python3

import os,sys
import feedparser
import hashlib
from log import Log
from color import Color
from time import strftime


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
        


class RSS():
    def __init__(self):
        self.HTML_path = '/home/eco/bin/apps/rss/html'
        self.feedlist_path = '/home/eco/bin/apps/rss/feedslist'
        self.feeds_path = '/home/eco/bin/apps/rss/feeds'
        self.template_path = '/home/eco/bin/apps/rss/templates/feed'
        self.feeds = {}     # Contains feeds: key: hashed url, value: parsed feed object
        self.log = Log()
        self.color = Color()


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


    def get_dir_contents(self, path):
        contents = []
        for path,dirs,files in os.walk(path):
            return files


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


    def hash(self, data):
        data = self.sanitize(data)
        data = self.encode(data)
        hashed = hashlib.sha224(data).hexdigest()
        return hashed


    def run(self):
        self.check_dir(self.feeds_path)
        self.check_dir(self.template_path)
        if not self.check_file(self.feedlist_path):
            self.log.error('No feedlist found at: %s... Quitting'%self.feedlist_path)

        feedlist = self.get_feedlist(self.feedlist_path)
        self.feeds = self.parse_feedlist(feedlist)
        html = GenerateHTML(self.template_path, self.feeds_path, self.HTML_path)
        html.run()


app = RSS()
app.run()
