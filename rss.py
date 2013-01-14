#!/usr/bin/python3

import os,sys
import feedparser
import hashlib
from log import Log
from color import Color
from time import strftime


class GenerateHTML(object):
    def __init__(self, data):
        pass


class RSS(object):
    def __init__(self):
        self.feedlist_path = '/home/eco/bin/apps/rss/feedslist'
        self.feeds_path = '/home/eco/bin/apps/rss/feeds'
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
            log.error('Failed to write to file: %s'%path)


    def parse_feed(self, feed):
        self.log.info('Parsing: %s'%feed)
        try:
            feed = feedparser.parse(feed)
            return feed
        except:
            self.log.error('Failed to parse feed: %s'%feed)
            return False


    def parse_feedlist(self, feedlist):
        feeds = {}
        for feed_url in feedlist:
            feed_parsed = self.parse_feed(feed_url)
            if feed_parsed:
                feed_url = self.encode(feed_url)
                feed_hash = self.hash(feed_url)
                feeds[feed_hash] = feed_parsed
                print(self.color.blue + feed_hash + self.color.reset)
                for f in feeds[feed_hash].entries:
                    print(self.color.red, f['title'], self.color.reset)
        return feeds


    def sanitize(self, var):
        # Strip file from blanks and newlines
        var = var.strip()
        return var


    def decode(self, data):
        data = self.sanitize(data)
        data = data.decode('utf-8')
        data = self.sanitize(data)
        return data


    def encode(self, data):
        data = self.sanitize(data)
        data = data.encode('utf-8')
        data = self.sanitize(data)
        return data


    def hash(self, data):
        data = self.sanitize(data)
        hashed = hashlib.sha224(data).hexdigest()
        return hashed


    def run(self):
        self.check_dir(self.feeds_path)
        if not self.check_file(self.feedlist_path):
            self.log.error('No feedlist found at: %s... Quitting'%self.feedlist_path)

        feedlist = self.get_feedlist(self.feedlist_path)
        self.feeds = self.parse_feedlist(feedlist)

        # Create dirs for every feed to contain the new messages
        for hash in self.feeds.keys():
            self.check_dir(self.feeds_path + '/' + hash)
            self.check_dir(self.feeds_path + '/' + hash + '/read')
            self.check_dir(self.feeds_path + '/' + hash + '/unread')






app = RSS()
app.run()
