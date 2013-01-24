StaticRSS
=========

StaticRSS is an rss reader that outputs static html files.  
This makes it extremely fast.   
It can be used on a server or you can just use it locally.  
  
Disclaimer: This script is a work in progress!!!  
This means it will probably make your computer explode ;)  
Use at your own risk!  

Dependencies:   
-------------
* beautifulsoup: https://github.com/bdoms/beautifulsoup    
* feedparser: https://code.google.com/p/feedparser/downloads/list    

Install on server:
------------------
<pre>
    -Clone re pository
        $ cd 
        $ git clone https://github.com/elcoco/static-rss.git.

    -Edit 'static-rss/config.py' to reflect your setup.
        Be sure to at least change:
            self.config_dir =           -The location of the script
            self.domain =               -Your domain eg. 'http://www.example.com'
            self.path_export_html =     -The path where the html files should be exported to
                                         eg. '/home/example/static-rss/html'

    -Change owner:group of static-rss directory to whatever user owns the webserver 
        eg: chown -R www-data:www-data /home/example/static-rss
        -If the HTML export dir is outside the static-rss directory you have to create it
         and change permissions manualy

    -Start static-rss as owner of webserver to create directories and database:
    $ su - www-data -c "PYTHONPATH=/usr/lib/python3 /usr/bin/python3 /home/example/static-rss/static-rss -p -g

    -Point your webserver to the export_html directory.

    -You can use cron to update your feeds, make sure it executes the script under the same user
     that owns the database and export directory
        As root: 
            $ crontab -e

        Add line to check every 10 minutes for new entries:
            */10  * * * * su - www-data -c "PYTHONPATH=/usr/lib/python3 /usr/bin/python3 /home/example/static-rss/static-rss -p -g"

        Restart cron
            $ service cron restart       (for ubuntu system)
            $ systemctl restart crond    (systemd/arch system)

    -A small php script is copied to 'export_dir/php/mark_read.php'.
     If the database is accessable to the webserver you can use this to mark your feeds
     as read.
</pre>

Install locally:
----------------

<pre>
    -Clone repository
    -Edit the config file to reflect your setup
    -run static-rss to create directories, database and html
    -point your browser to the index.html
    -Make a cronjob for automatic updating
</pre>
