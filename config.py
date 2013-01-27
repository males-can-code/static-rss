#!/usr/bin/python3
import os

class Config(object):
    def __init__(self):
        self.max_chars_per_page     = 10000    # Max amount of characters a page contains
        self.max_entries_in_sidebar = 30       # Max amount of entries in right sidebar
        self.entry_ttl              = 1        # When to delete entries in days, False to disable 
                                               # (This will make generating html a lot more time consuming)
        self.links_target           = '_blank' # Wether to open links in a new window or not '_blank' = new, '_self' = same

        # List of blacklisted tags and attributes for content
        self.invalid_tags = ['script', 'html', 'body', 'strong', 'hr']
        self.invalid_attr = ['class', 'id', 'name', 'style', 'border', 'width', 'height']

        # This switches a couple of page elements on or off
        self.switch = {}
        self.switch['mark_read']        = True # Display mark read button on page
        self.switch['mark_all_read']    = True # Display mark all read button on page
        self.switch['update_feeds']     = True # Display update feeds button on page
        self.switch['auto_mark_read']   = True # Automatically mark feed read on opening page
        self.switch['auto_refresh']     = 120  # Automatic page refresh in seconds or False to disable

        self.domain                = 'http://rss.opentbc.nl'         # eg: 'http://example.com'
        self.app_dir               = '/home/eco/bin/apps/static-rss' # eg: '/home/user/static-rss'

        # Should be something like '/var/www/static-rss' or '/home/user/static-rss/html'
        # If /tmp is tmpfs, you can also do '/tmp/static-rss' for incredible speed improvements
        # Check README.md for a brief explanation about tmpfs
        self.path_export_html      = '/tmp/static-rss/html'          
        self.path_db               = '/tmp/static-rss/static-rss.sqlite'    # Path to sqlite database

        self.path_template_feed    = self.app_dir + '/templates/feed.html'  # Path to the main template
        self.path_css              = self.app_dir + '/css/stylesheet.css'
        self.path_php              = self.app_dir + '/php'
        self.path_script_update    = self.app_dir + '/php/update.php'
        self.path_script_mark_read = self.app_dir + '/php/mark_read.php'
        self.path_script_subscribe = self.app_dir + '/php/subscribe.php'
        self.path_db_manager       = self.app_dir + '/php/phpliteadmin.php'
        self.path_favicon          = self.app_dir + '/pics/favicon.ico'

        # Appart from just adding feeds to the database you can also enter them here as: ['url', 'group']
        self.feeds = [['http://www.webupd8.org/feeds/posts/default',                                    'linux'], 
                      ['http://www.osnews.com/files/recent.xml',                                        'linux'], 
                      ['http://inconsolation.wordpress.com/feed/',                                      'linux'], 
                      ['http://librenix.com/rss/',                                                      'linux'], 
                      ['http://feeds.feedburner.com/d0od',                                              'linux'], 
                      ['http://feeds.feedburner.com/ostatic',                                           'linux'], 
                      ['http://www.tuxmachines.org/node/feed',                                          'linux'], 
                      ['http://tweakers.net/feeds/mixed.xml',                                           'linux'], 
                      ['http://feeds.webwereld.nl/webwereld',                                           'linux'], 
                      ['http://www.phoronix.com/rss.php',                                               'linux'], 
                      ['http://feeds.feedburner.com/Linuxers?format=xml',                               'linux'], 
                      ['http://lxer.com/module/newswire/headlines.rss',                                 'linux'], 
                      ['http://rss.feedsportal.com/c/32569/f/491734/index.rss',                         'linux'], 
                      ['http://feeds.feedburner.com/thepowerbase?format=xml',                           'linux'], 
                      ['http://feeds.feedburner.com/unixmenhowtos?format=xml',                          'linux'], 

                      ['http://www.nasa.gov/rss/lg_image_of_the_day.rss',                               'space'], 
                      ['http://www.nasa.gov/rss/chandra_images.rss',                                    'space'], 
                      ['http://www.esa.int/rss/TopNews.xml',                                            'space'], 
                      ['http://www.nasa.gov/directorates/somd/reports/iss_reports/iss_reports.rss',     'space'], 
                      ['http://www.nasa.gov/rss/breaking_news.rss',                                     'space'], 
                      ['http://www.nasa.gov/mission_pages/SOFIA/sofia-newsandfeatures-RSS.rss',         'space'], 
                      ['http://www.nasa.gov/rss/solar_system.rss',                                      'space'], 
                      ['http://www.nasa.gov/rss/universe.rss',                                          'space'], 
                      ['http://www.nasa.gov/mission_pages/kepler/news/kepler-newsandfeatures-RSS.rss',  'space'], 

                      ['https://bbs.archlinux.org/extern.php?action=feed&tid=92895&type=atom',          'threads'],
                      ['https://bbs.archlinux.org/extern.php?action=feed&tid=155476&type=atom',         'threads'],

                      ['http://feeds.bbci.co.uk/news/rss.xml',                                          'news'],
                      ['http://www.haarlemsdagblad.nl/?service=rss',                                    'news'],
                      ['http://www.haarlemsdagblad.nl/nieuws/regionaal/?service=rss',                   'news'],
                      ['http://feeds.nos.nl/nosnieuwsalgemeen',                                         'news'],
                      ['http://nrc.nl/rss.php',                                                         'news'],
                      ['http://www.nu.nl/feeds/rss/algemeen.rss',                                       'news'],
                      ['http://lifehacker.com/index.xml',                                               'news'],

                      ['http://elementaryos.org/journal/rss.xml',                                       'projects'],
                      ['http://www.raspberrypi.org/feed',                                               'projects'],
                      ['http://themagpi.wordpress.com/feed/',                                           'projects'],
                      ['https://www.haiku-os.org/rss.xml',                                              'projects'],
                      ['https://www.tizen.org/blogs/feed',                                              'projects'],
                      ['http://www.cyanogenmod.com/feed',                                               'projects'],
                      ['http://fritzing.org/news/feeds/rss/',                                           'projects'],

                      ['http://quicksurf.com/?feed=ogg&amp;cat=141',                                    'podcasts'],
                      ['http://feeds.feedburner.com/linuxoutlaws',                                      'podcasts']]
