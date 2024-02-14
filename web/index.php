<?php
    require 'api/db.php';
    require 'api/functions.php';
    $concerts = get_all_concerts($conn);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/style.css">
    <title>Konserter i Stockholm</title>
</head>
<body>
   <?php require 'header.php'; ?>
    <div class="container">
        <ul class='concert-list'>
            <?php
                $prev_date = 0;
                $prev_venue = "";

                while ($concert = $concerts->fetch_assoc()):
                    $sql_date = $concert['date'];
                    $date = date('D d M Y', strtotime($sql_date));
                    $venue = $concert['venue'];

                    if ($date != $prev_date): ?>
                        <h4 class='concert-date'>
                            <?php
                                secure_echo($date);
                            ?>
                        </h4>
                    <?php $prev_date = $date; endif; ?>

                    <div class="concert">
                        <details>
                            <summary>
                                <span class='event-venue'>
                                    <?php secure_echo($venue); ?>
                                </span>
                                -
                                <span class='event-title'>
                                    <a href="<?php secure_echo($concert['url']); ?>">
                                        <span class="event-title">
                                        <?php secure_echo($concert['title']); ?>
                                        </span>
                                    </a>
                                </span>
                            </summary>
                            <p><?php secure_echo($concert['description']); ?></p>
                        </details>
                    </div>

                <?php endwhile; ?>
        </ul>
    </div>
</body>
</html>