<?php
    $go_back = $_GET["go_back"]; 
    $handle = popen('LANG=en_US.UTF-8 $app_dir/static-rss -p', 'r');
    pclose ($handle);
    header ("location: $go_back");
?>

