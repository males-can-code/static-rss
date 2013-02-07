<?php
    $go_back = $_GET["go_back"]; 
    $handle = popen('LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss -p >> /tmp/StaticRSS.log 2>&1 &', 'r');
    $line = "";
    pclose ($handle);
    
    while (true) 
    {
        if (! file_exists('/var/www/opentbc.nl/static-rss/index.html')) 
        { 
            sleep(1); 
        }
        else 
        {
            break;
        }
    }

    header ("location: $go_back");
?>

