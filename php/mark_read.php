<?php
    $hash = $_GET["hash"];
    $go_back = $_GET["go_back"];
    $mode = $_GET["mode"];

    if ($hash == 'all') 
    {
        $handle = popen("LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --mark-all-read >> /tmp/StaticRSS.log 2>&1", 'r');
    }
    else 
    {
        $handle = popen("LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --mark-read=$hash >> /tmp/StaticRSS.log 2>&1", 'r');
    }
    pclose ($handle);
    
    if ($mode != 'silent')
    {
        header ("location: $go_back");
    }
?>
