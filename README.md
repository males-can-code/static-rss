StaticRSS
=========

StaticRSS is an rss reader that outputs static html files.
It can be used on a server or you can just use it locally.

Disclaimer: This script is a work in progress!!!
This means it will probably make your computer explode ;)
Use at your own risk!


Install on server:

    -Clone repository
        git clone https://github.com/elcoco/static-rss.git.

    -Change owner of static-rss, static-rss/php to whatever user owns the webserver 
        eg: chown www-data:www-data ~/static-rss

    -Edit 'static-rss/config.py' to reflect your setup.
        Be sure to at least change:
            self.config_dir =       -The location of the script
            self.domain =           -Your domain eg. 'http://www.example.com'
            self.path_export_html = -The path where the html files should be exported to
                                      eg. '/var/www/static-rss'

    -Point your webserver to the export_html directory.
    -You can use cron to update your feeds, make sure it runs under the same user
     that owns the database
    -A small php script is copied to export_dir/php/mark_read.php.
     If the database is accessable to the webserver you can use this to mark your feeds
     as read.


Install locally:

    -Clone repository
    -Edit the config file to reflect your setup
    -run static-rss to create directories, database and html
    -point your browser to the index.html
    -Make a cronjob for automatic updating
