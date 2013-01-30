<?php
    $hash = $_GET["hash"];
    $go_back = $_GET["go_back"];

    if ($hash) 
    {
        $handle = popen("LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --del-feed=$hash >> /tmp/StaticRSS.log 2>&1", 'r');
    }
    pclose ($handle);
    

    header ("location: $go_back");
?>
