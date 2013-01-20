<?php

    function isValidMd5($md5)
    {
        return !empty($md5) && preg_match('/^[a-f0-9]{32}$/', $md5);
    }

    $hash = $_GET["hash"];
    $go_back = $_GET["go_back"];

    try 
    {
        $db = new PDO('sqlite:/home/eco/bin/apps/static-rss/database/static-rss.sqlite');

        if ($hash == 'all') 
        {
            $sth = $db->prepare("update entries set 'read' = 'True'");
        }
        elseif (isValidMd5($hash) == 0) 
        {
            $sth = $db->prepare("update entries set 'read' = 'True' where feed_hash = :parameter");
            $sth->bindParam(':parameter', $hash, PDO::PARAM_STR);
        }

        $sth->execute();
        $db = NULL;
    }

    catch(PDOException $e) 
    {
        print 'Exception : '.$e->getMessage();
    }


    $handle = popen('LANG=en_US.UTF-8 /home/eco/bin/apps/static-rss/static-rss --gen-html >> /tmp/StaticRSS.log 2>&1', 'r');
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

