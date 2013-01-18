<?php
    /*** make it or break it ***/
    error_reporting(E_ALL);

    try
    {
        /*** create the database file in /tmp ***/
        $dbh = PDO("sqlite:/home/eco/apps/static-rss/static-rss.sqlite");

        /*** set all errors to excptions ***/
        $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        /*** begin a transaction ***/
        $dbh->beginTransaction();

        $dbh->exec("UPDATE 'entries' SET 'read' = 'True' WHERE '7d2efe20a061111e51d4c0bdf09a6c38294b9197039b9fdf2eb6b682';");

        /*** commit the INSERTs ***/
        $dbh->commit();

        echo 'done';
    }
    catch(Exception $e)
    {
        echo $e->getMessage();
    }
?>
