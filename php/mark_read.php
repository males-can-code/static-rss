<?php
    //$hash=$_GET["hash"];
    $hash = 'all';
    echo $hash;

    if ($hash == 'all') {
        $query = "UPDATE 'entries' SET 'read' = 'True';";
        echo $query;
        echo 'all';
    }
    else {
        $query = "UPDATE 'entries' SET 'read' = 'True' where 'url_hash' = '$hash';";
        echo $query;
        echo $hash;
    }

    $db = new PDO('sqlite:/home/eco/bin/apps/static-rss/static-rss.sqlite');
    $db->exec($query);

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

