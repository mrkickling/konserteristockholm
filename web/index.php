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

        <div class="search-form">
            <form action="">
                <input type="text" name="q" placeholder="Sök på artist eller lokal">
                <input type="submit" value="Sök">
            </form>
        </div>

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
                        <h4 class='concert-date'>
                            <?php
                                secure_echo($date);
                            ?>
                        </h4>
                    <?php $prev_date = $date; endif; ?>

                    <div class="concert">
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

                        <?php if (isset($_SESSION['isAdmin']) && $_SESSION['isAdmin']): ?>
                            <form class="hide-form" method="post" action="api/hide.php">
                                <input name="id" type="hidden" value="<?php secure_echo($concert['id']); ?>">
                                <button>Hide</button>
                            </form>
                        <?php endif; ?>

                    </div>

                <?php endwhile; ?>
            </ul>
        </div>
    </body>
</html>