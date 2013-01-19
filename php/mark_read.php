<?php
    $hash=$_GET["hash"];

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
?>

