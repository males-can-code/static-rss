StaticRSS
=========
StaticRSS is an rss reader written in python3 that outputs static html files.  
This makes it ideal for webservers on slow connections.   
  
**Disclaimer:** This script is a work in progress!!!  
This means it will probably make your computer explode ;)  
Use at your own risk!  

## Dependencies:   
* **beautifulsoup:** https://github.com/bdoms/beautifulsoup    
* **feedparser:** https://code.google.com/p/feedparser/downloads/list    

## Install:
#### Clone repository  
<pre>
$ cd  
$ git clone https://github.com/elcoco/static-rss.git    
</pre>
#### Edit 'static-rss/config.py' to reflect your setup.
Be sure to at least change:   

<pre>
self.config_dir =            -The location of the script eg. '/home/example_user/static-rss'  
self.domain =                -Your domain eg. 'http://www.example.com'   
self.path_export_html =      -The path where the html files should be exported to     
                              eg. '/home/example_user/static-rss/html' or '/var/www/static-rss'  
</pre>

#### Change permissions
Change **owner:group** of static-rss directory to whatever user owns the webserver    
If the path_export_html is outside the static-rss directory you have to create it     
and change those permissions also    

<pre>
$ chown -R www-data:www-data /home/example/static-rss 
</pre>   

Execute static-rss as owner of webserver to create directories and database:  

<pre>
$ su - www-data -c "PYTHONPATH=/usr/lib/python3 /usr/bin/python3 /home/example/static-rss/static-rss -p -g
</pre>

#### Done!
Point your webserver to the path_export_html directory or your domain.    

## Extra
#### Update feeds
You can use cron to update your feeds, make sure it executes the script under the same user   
that owns the database and export directory.   

<pre>
$ su
$ crontab -e

*/10  * * * * su - www-data -c "PYTHONPATH=/usr/lib/python3 /usr/bin/python3 /home/example/static-rss/static-rss -p -g"

$ service cron restart       (for ubuntu system)
$ systemctl restart crond    (systemd/arch system)
</pre>

#### Not so static stuff
A couple of small php scripts can optionaly be used.  
If the database is accessable to the webserver you can use them to mark your feeds   
read or to update your feeds from the web.  

#### TMPFS:    
To make static-rss faster you can use a tmpfs.    
<pre>
self.path_export_dir = '/tmp/static-rss/html'
self.path_db = '/tmp/static-rss/database'   
</pre>

To create a tmpfs on /tmp:

<pre>
$ vi /etc/fstab
tmpfs   /tmp         tmpfs   nodev,nosuid,size=500M          0  0
</pre>

#### Firefox
For an easy way of adding feeds to static-rss, you can create a bookmark in firefox with the following content:   

<pre>
javascript:{var group=prompt("Enter group","default");window.location.href="[domain]/php/subscribe.php?url="+document.URL+'&group='+group;}
</pre>

Repace [domain] with your domain    
