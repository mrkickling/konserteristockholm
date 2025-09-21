<?php session_start(); ?>
<?php 
    require 'api/db.php';
    require 'api/functions.php';

    if (isset($_SESSION['isAdmin']) && isset($_POST['id'])) {
        if (isset($_POST['accept'])) {
            show_concert($conn, $_POST['id']);
            header('Location: admin.php');
        }

        if (isset($_POST['reject'])) {
            delete_concert($conn, $_POST['id']);
            header('Location: admin.php');
        }
    }
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

    <?php
        if (!isset($_SESSION['isAdmin'])):
    ?>
            <div class="info">
                <h2>Log in</h2>
                <p>
                    <form action="api/auth.php" method="post" id="login-form">
                        <input type="text" name="username" placeholder="Username"><br>
                        <input type="password" name="password" placeholder="Password"><br>
                        <input type="submit" value="Logga in">
                    </form>
                </p>
            </div>
    <?php
        else:
            $concerts = get_unapproved_concerts($conn);
    ?>

        <?php
            while ($concert = $concerts->fetch_assoc()):
                $sql_date = $concert['date'];
                $date = date('D d M Y', strtotime($sql_date));
                $venue = $concert['venue'];
        ?>

            <div class="concert-container">
                    <div class="concert">
                        <span class='event-title'>
                            <b>Concert:</b> <?php secure_echo($concert['title']); ?><br>
                            <b>URL:</b> <?php secure_echo($concert['url']) ?>
                            </a>
                        </span>

                        <br>

                        <div class="event-venue-container">
                            <span class='event-venue'>
                                <?php secure_echo($venue); ?>
                            </span>
                            <span class='event-venue'>
                                | <?php secure_echo($date); ?>
                            </span>
                        </div>
                        <form method="post">
                            <input type="hidden" name="id" value="<?php secure_echo($concert['id']) ?>">
                            <input name="reject" class="reject-button" type="submit" value="Reject">
                            <input name="accept" class="accept-button" type="submit" value="Accept">
                        </form>
                    </div>
                </div>
            </div>

        <?php endwhile; ?>

    <?php
        endif;
    ?>

    </div>
</body>
</html>

