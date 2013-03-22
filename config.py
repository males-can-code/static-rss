#!/usr/bin/python3
import os

class Config(object):
    def __init__(self):
        self.links_target               = '_blank' # Open links in a new window or not '_blank' = new, '_self' = same
        self.entries_per_page           = 10        # Max amount of entries a page will contain
        self.max_pages                  = 10       # Max amount of pages that will be generated, keep this low as this will improve performance
        self.max_entries_per_feed_in_db = 200      # Max amount of entries per feed before being deleted from database

        # List of blacklisted tags and attributes for content
        self.invalid_tags = ['script', 'html', 'body', 'strong', 'hr', 'font']
        self.invalid_attr = ['class', 'align', 'id', 'name', 'style', 'border', 'width', 'height', 'color']

        # This switches a couple of page elements on or off
        self.switch = {}
        self.switch['auto_mark_read']     = True # Automatically mark feed read on opening page
        self.switch['auto_refresh']       = 600  # Automatic page refresh in seconds or False to disable
        self.switch['menu']               = True # An awesome jquery menu that remembers state using cookies
        self.switch['php_buttons']        = True # The php buttons on top of page (del feed, mark read, mark all read)

        self.domain  = '//rss.opentbc.nl'         # eg: '//example.com' (leave the http: cause chromium will start complaining about insecure content
        self.app_dir = '/home/eco/bin/apps/static-rss' # Location of the program, eg: '/home/user/static-rss'

        # Should be something like '/var/www/static-rss'
        # If /tmp is tmpfs, you can also do '/tmp/static-rss' for speed improvements
        # Check README.md for a brief explanation about tmpfs
        self.path_export_html      = '/tmp/static-rss'          
        self.path_export_html_tmp  = '/tmp/static-rss-tmp' # generate html to tmp dir and copy it to path_export_html

        # Where we can find certain files
        self.path_db               = self.app_dir + '/database/static-rss.sqlite' # Path to sqlite database
        self.path_template_feed    = self.app_dir + '/templates/feed.html'        # Path to the main template
        self.path_template_menu    = self.app_dir + '/templates/menu.html'        # Path to the menu template
        self.path_template_page    = self.app_dir + '/templates/page.html'        # generates all entries in page
        self.path_template_index   = self.app_dir + '/templates/index.html'       # This template redirects to a feed
        self.path_stylesheet       = self.app_dir + '/css/dark.css'
        self.path_css              = self.app_dir + '/css'
        self.path_php              = self.app_dir + '/php'
        self.path_js               = self.app_dir + '/js'
        self.path_favicon          = self.app_dir + '/pics/favicon.ico'

        # Appart from just adding feeds to the database you can also enter them here as: ['url', 'group']
        # They will be automatically added to the database also if you remove them from the database
        # You can leave this var empty, 'self.feeds = []'
        self.feeds = [['http://www.webupd8.org/feeds/posts/default', 'linux'], 
                      ['http://www.osnews.com/files/recent.xml',     'linux']]
