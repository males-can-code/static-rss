<?php
    $url = $_GET["url"];
    $group = $_GET["group"];

    $handle = popen("LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --subscribe=$url --group=$group >> /tmp/StaticRSS.log 2>&1 &", 'r');
    pclose ($handle);
    header ("location: $url");
?>

