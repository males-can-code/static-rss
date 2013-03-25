<?php
    $url = $_GET["url"];
    $group = $_GET["group"];

    $handle = popen("LANG=en_US.UTF-8 $app_dir/static-rss --subscribe=$url --group=$group", 'r');
    pclose ($handle);
    header ("location: $url");
?>

