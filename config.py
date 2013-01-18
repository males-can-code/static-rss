#!/usr/bin/python3
import os

class Config(object):
    def __init__(self):
        self.config_dir                        = os.getenv('HOME') + '/bin/apps/static-rss'

        self.path_db                           = self.config_dir + '/rss.db'
        self.path_export_html                  = self.config_dir + '/html'
        self.path_template_entry_read          = self.config_dir + '/templates/entry_read.html'
        self.path_template_entry_unread        = self.config_dir + '/templates/entry_unread.html'
        self.path_template_feed                = self.config_dir + '/templates/feed.html'
        self.path_template_feed_list_read      = self.config_dir + '/templates/feed_urls_read.html'
        self.path_template_feed_list_unread    = self.config_dir + '/templates/feed_urls_unread.html'
        self.path_template_entry_list_read     = self.config_dir + '/templates/entry_list_read.html'
        self.path_template_entry_list_unread   = self.config_dir + '/templates/entry_list_unread.html'
        self.path_template_page_link           = self.config_dir + '/templates/page_links.html'
        self.path_template_group               = self.config_dir + '/templates/group.html'
        self.path_css                          = self.config_dir + '/css/stylesheet.css'


        self.feeds                             = ['http://www.webupd8.org/feeds/posts/default', 
                                                  'http://www.raspberrypi.org/feed', 
                                                  'http://www.nasa.gov/rss/lg_image_of_the_day.rss', 
                                                  'http://www.osnews.com/files/recent.xml', 
                                                  'http://inconsolation.wordpress.com/feed/', 
                                                  'http://iloveubuntu.net/rss.xml', 
                                                  'http://feeds.bbci.co.uk/news/rss.xml']

        self.groups                            = ['linux', 
                                                  'news']
