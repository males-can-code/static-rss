<?php
    $hash = $_GET["hash"];
    $go_back = $_GET["go_back"];
    $mode = $_GET["mode"];

    if ($hash == 'all') 
    {
        $handle = popen("LANG=en_US.UTF-8 $app_dir/static-rss --mark-all-read", 'r');
    }
    else 
    {
        $handle = popen("LANG=en_US.UTF-8 $app_dir/static-rss --mark-read=$hash", 'r');
    }
    pclose ($handle);
    
    if ($mode != 'silent')
    {
        header ("location: $go_back");
    }
?>
