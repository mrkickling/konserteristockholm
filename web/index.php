<?php
    require 'api/db.php';
    require 'api/functions.php';
    session_start();

    $q = "";
    if (isset($_GET['q'])) {
        $q = $_GET['q'];
    }
    $concerts = get_concerts($conn, $q);
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
            <ul class='concert-list'>
            <?php
                $prev_date = 0;
                $prev_venue = "";

                if ($concerts->num_rows == 0):
                    echo "
                        <p>
                            Hittade inga konserter för din sökning.
                            <br>
                            Sök på nåt annat eller se <a href='/'>alla konserter</a>.
                        </p>
                        ";
                endif;

                while ($concert = $concerts->fetch_assoc()):
                    $sql_date = $concert['date'];
                    $date = date('D d M Y', strtotime($sql_date));
                    $venue = $concert['venue'];

                    if ($date != $prev_date): ?>
                        <div class="concert-header-container">
                            <h4 class='concert-date-header'>
                                <span class="date-icon material-symbols-outlined">
                                    calendar_today
                                </span>
                                <span class="concert-date">
                                    <?php
                                        secure_echo($date);
                                    ?>
                                </span>
                            </h4>
                        </div>
                    <?php $prev_date = $date; endif; ?>

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
                        </div>
                    </div>

                <?php endwhile; ?>
            </ul>
        </div>
        <script src="assets/scrolling.js"></script>
    </body>
</html>