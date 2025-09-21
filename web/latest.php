<?php
    require 'api/db.php';
    require 'api/functions.php';
    session_start();

    $concerts = get_latest_released_concerts($conn);
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="assets/style.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0" />
        <title>Konserter i Stockholm</title>
    </head>
    <body>
    <?php require 'header.php'; ?>

        <div class="container">
            <div class="concert-date-container">
                <h4 class='concert-date-header'>
                    Senaste släpp
                </h4>
            </div>

            <ul class='concert-list'>

            <?php
                while ($concert = $concerts->fetch_assoc()):
                    $sql_date = $concert['date'];
                    $date = date('D d M Y', strtotime($sql_date));
                    $venue = $concert['venue'];
            ?>

                <div class="concert-container">
                        <div class="concert">
                            <span class='event-title'>
                                <a href="<?php secure_echo($concert['url']); ?>">
                                    <?php secure_echo($concert['title']); ?>
                                </a>
                            </span>

                            <br>

                            <div class="event-venue-container">
                                <span class="material-symbols-outlined location-icon">
                                    location_on
                                </span>
                                <span class='event-venue'>
                                    <?php secure_echo($venue); ?>
                                </span>
                                <span class='event-venue'>
                                    | <?php secure_echo($date); ?>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

            <?php endwhile; ?>
            </ul>
        </div>
    </body>
</html>