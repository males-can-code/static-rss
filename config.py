#!/usr/bin/python3
import os

class Config(object):
    def __init__(self):

        self.max_chars_per_page = 10000
        self.max_entries_in_sidebar = 20
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


        self.feeds                             = [['http://www.webupd8.org/feeds/posts/default',                'linux'], 
                                                  ['http://www.osnews.com/files/recent.xml',                    'linux'], 
                                                  ['http://inconsolation.wordpress.com/feed/',                  'linux'], 
                                                  ['http://librenix.com/rss/',                                  'linux'], 
                                                  ['http://feeds.feedburner.com/d0od',                          'linux'], 
                                                  ['http://feeds.feedburner.com/ostatic',                       'linux'], 
                                                  ['http://www.tuxmachines.org/node/feed',                      'linux'], 
                                                  ['http://tweakers.net/feeds/mixed.xml',                       'linux'], 
                                                  ['http://feeds.webwereld.nl/webwereld',                       'linux'], 
                                                  ['http://www.phoronix.com/rss.php',                           'linux'], 
                                                  ['http://feeds.feedburner.com/Linuxers?format=xml',           'linux'], 
                                                  ['http://lxer.com/module/newswire/headlines.rss',             'linux'], 
                                                  ['http://rss.feedsportal.com/c/32569/f/491734/index.rss',     'linux'], 
                                                  ['http://feeds.feedburner.com/thepowerbase?format=xml',       'linux'], 
                                                  ['http://feeds.feedburner.com/unixmenhowtos?format=xml',      'linux'], 

                                                  ['http://www.nasa.gov/rss/lg_image_of_the_day.rss',                               'space'], 
                                                  ['http://www.nasa.gov/rss/chandra_images.rss',                                    'space'], 
                                                  ['http://www.esa.int/rss/TopNews.xml',                                            'space'], 
                                                  ['http://www.nasa.gov/directorates/somd/reports/iss_reports/iss_reports.rss',     'space'], 
                                                  ['http://www.nasa.gov/rss/breaking_news.rss',                                     'space'], 
                                                  ['http://www.nasa.gov/mission_pages/SOFIA/sofia-newsandfeatures-RSS.rss',         'space'], 
                                                  ['http://www.nasa.gov/rss/solar_system.rss',                                      'space'], 
                                                  ['http://www.nasa.gov/rss/universe.rss',                                          'space'], 
                                                  ['http://www.nasa.gov/mission_pages/kepler/news/kepler-newsandfeatures-RSS.rss',  'space'], 

                                                  ['https://bbs.archlinux.org/extern.php?action=feed&tid=92895&type=atom',    'threads'],
                                                  ['https://bbs.archlinux.org/extern.php?action=feed&tid=155476&type=atom',   'threads'],

                                                  ['http://feeds.bbci.co.uk/news/rss.xml',                          'news'],
                                                  ['http://www.haarlemsdagblad.nl/?service=rss',                    'news'],
                                                  ['http://www.haarlemsdagblad.nl/nieuws/regionaal/?service=rss',   'news'],
                                                  ['http://feeds.nos.nl/nosnieuwsalgemeen',                         'news'],
                                                  ['http://nrc.nl/rss.php',                                         'news'],
                                                  ['http://www.nu.nl/feeds/rss/algemeen.rss',                       'news'],
                                                  ['http://lifehacker.com/index.xml',                               'news'],

                                                  ['http://elementaryos.org/journal/rss.xml',                           'projects'],
                                                  ['http://www.raspberrypi.org/feed',                                   'projects'],
                                                  ['http://themagpi.wordpress.com/feed/',                               'projects'],
                                                  ['https://www.haiku-os.org/rss.xml',                                  'projects'],
                                                  ['https://www.tizen.org/blogs/feed',                                  'projects'],
                                                  ['http://www.cyanogenmod.com/feed',                                   'projects'],
                                                  ['http://fritzing.org/news/feeds/rss/',                               'projects'],

                                                  ['http://quicksurf.com/?feed=ogg&amp;cat=141',                        'podcasts'],
                                                  ['http://feeds.feedburner.com/linuxoutlaws',                          'podcasts']]

        self.groups                            = ['linux', 'projects', 'news', 'space', 'threads', 'reddit']
