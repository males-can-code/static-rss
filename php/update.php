<?php
    $handle = popen('LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss >> /tmp/StaticRSS.log 2>&1', 'r');
    $line = "";

    while (false !== ($char = fgetc($handle))) 
    {
        if ($char == "\r") 
        {
            // You could now parse the $line for status information.
            echo "$line\n";
            $line = "";
        }

        else {
            $line .= $char;
        }

        ob_flush();
        flush();

    }

    pclose ($handle);
    
    while (true) 
    {
        if (! file_exists('/var/www/opentbc.nl/static-rss/index.html')) 
        { 
            sleep(.2); 
        }
        else 
        {
            break;
        }
    }

    header ("location: $go_back");
?>

