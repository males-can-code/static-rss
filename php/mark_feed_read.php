<?php
  try
  {
    //open the database
    $db = new PDO('sqlite:/home/eco/bin/apps/static-rss/static-rss.sqlite');

    $db->exec("UPDATE 'entries' SET 'read' = 'True';");

    // close the database connection
    $db = NULL;
  }
  catch(PDOException $e)
  {
    print 'Exception : '.$e->getMessage();
  }
?>
