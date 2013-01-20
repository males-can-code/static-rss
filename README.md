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

    -Change group of static-rss to whatever user owns the webserver 
        eg: chown -R insert_user_here:www-data ~/static-rss

    -Edit 'static-rss/config.py' to reflect your setup.
        Be sure to at least change:
            self.config_dir =       -The location of the script
            self.domain =           -Your domain eg. 'http://www.example.com'
            self.path_export_html = -The path where the html files should be exported to
                                      eg. '/var/www/static-rss'

    -Create export directory
        $ mkdir ~/static-rss/html                       #or whatever you configured in config.py
        $ chown -R www-data:www-data ~/static-rss/html

    -Create database directory
        $ mkdir ~/static-rss/database
        $ chown -R www-data:www-data ~/static-rss/database

    -Point your webserver to the export_html directory.

    -You can use cron to update your feeds, make sure it executes the script under the same user
     that owns the database and export directory

        as root: 
            $ crontab -e

        add line:
            */10  * * * * su - www-data -c "PYTHONPATH=/usr/lib/python3 /usr/bin/python3 /home/eco/bin/apps/static-rss/static-rss"

        restart cron
            $ service cron restart       (for ubuntu system)
            $ systemctl restart crond    (systemd/arch system)

    -A small php script is copied to export_dir/php/mark_read.php.
     If the database is accessable to the webserver you can use this to mark your feeds
     as read.


Install locally:

    -Clone repository
    -Edit the config file to reflect your setup
    -run static-rss to create directories, database and html
    -point your browser to the index.html
    -Make a cronjob for automatic updating
