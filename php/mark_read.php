<?php
    function isValidMd5($md5)
    {
        return !empty($md5) && preg_match('/^[a-f0-9]{32}$/', $md5);
    }


    $hash = $_GET["hash"];
    $go_back = $_GET["go_back"];

    if ($hash == 'all') 
    {
        $handle = popen("LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --mark-all-read >> /tmp/StaticRSS.log 2>&1", 'r');
        echo $hash;
    }
    else 
    {
        $handle = popen("LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --mark-read=$hash >> /tmp/StaticRSS.log 2>&1", 'r');
        echo $hash;
    }

    pclose ($handle);
    

    if ($hash != 'all')
    {
        while (true) 
        {
            if (! file_exists('/var/www/opentbc.nl/static-rss/feeds/'.$hash.'/page_1.html')) 
            { 
                sleep(.2); 
            }
            else 
            {
                break;
            }
        }
    }

    header ("location: $go_back");
?>

