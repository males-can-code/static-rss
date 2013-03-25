<?php
    $hash = $_GET["hash"];
    $go_back = $_GET["go_back"];

    if ($hash) 
    {
        $handle = popen("LANG=en_US.UTF-8 $app_dir/static-rss --del-feed=$hash", 'r');
    }
    pclose ($handle);
    

    header ("location: $go_back");
?>
