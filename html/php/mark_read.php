<?php
    $hash=$_GET["hash"];
    $go_back=$_GET["go_back"];

    if ($hash == 'all') {
        $query = "UPDATE 'entries' SET 'read' = 'True';";
    }
    else {
        $query = "UPDATE 'entries' SET 'read' = 'True' where 'url_hash' = '$hash';";
    }


    try {
        //open the database
        $db = new PDO('sqlite:/home/eco/bin/apps/static-rss/static-rss.sqlite');
        $db->exec($query);

        // close the database connection
        $db = NULL;

    }

    catch(PDOException $e) {
        print 'Exception : '.$e->getMessage();
    }

    #$last_line = system('/home/eco/bin/apps/static-rss/static-rss --gen-html', $retval);
    #echo $last_line;
    header ("location: $go_back");
?>

