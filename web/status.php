<?php
    require 'api/db.php';
    require 'api/functions.php';
    session_start();

    $venues = get_venues($conn);
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

        <?php if (isset($_SESSION['isAdmin']) && $_SESSION['isAdmin']): ?>
            <form action="api/auth.php" method="post">
                <input type="hidden" name="logout">
                <input type="submit" value="Log out">
            </form>
        <?php endif; ?>

            <ul class='concert-list'>
            <?php

                while ($venue = $venues->fetch_assoc()): 
                    $color = 'green';
                    if ($venue['up'] == 0) $color = 'red';
                ?>

                    <div class="concert">
                            <span class='event-venue' style="color:<?php echo $color ?>">
                                <?php secure_echo($venue['name']); ?>
                            </span>
                            
                            <span class='event-title'>
                                -
                                <?php if ($venue['up'] == 1): echo "UP"; endif; ?>
                                <?php if ($venue['up'] == 0): echo "DOWN since"; endif; ?>
                                                                        
                                <?php secure_echo($venue['latest_sync']); ?>

                            </span>
                    </div>

                <?php endwhile; ?>
            </ul>
        </div>
    </body>
</html>