<?php
    require 'api/db.php';
    require 'api/functions.php';
    session_start();

    if (!isset($_SESSION['isAdmin'])) {
        header('Location: index.php');
    }

    if (isset($_POST['new-concert'])) {
        $concert = array(
            'title'=> $_POST['title'],
            'date' => $_POST['date'],
            'venue' => $_POST['venue'],
            'url' => $_POST['url']
        );
        create_static_concert($conn, $concert);
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="assets/style.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0" />
        <title>Konserter i Stockholm</title>
        <meta name="description" content="Här samlas framtida konserter i Stockholm. Se varje dags utbud eller sök på artist och konsertlokal.">
    </head>
    <body>
    <?php require 'header.php'; ?>
        <div class="container">
            <h2>Lägg till konsert</h2>
            <form action="new_concert.php" method="post">
                Titel
                <input type="text" name="title"><br>
                Scen
                <input type="text" name="venue"><br>
                URL
                <input type="text" name="url"><br>
                Datum
                <input type="date" name="date"><br>
                <input type="submit" name="new-concert" value="Lägg till">
            </form>
        </div>
        <script src="assets/scrolling.js"></script>
    </body>
</html>