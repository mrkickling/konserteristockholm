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
    <header>
        <a href="index.php">
            <h3>♬ Konserter i Stockholm ♬</h3>
        </a>
        <a href="info.php" class="info-link">?</a>
    </header>
    <div class="container">
        <ul class='concert-list'>
            <?php
                $prev_date = 0;
                while ($concert = $concerts->fetch_assoc()):
                    $sql_date = $concert['date'];
                    $date = date('d M Y', strtotime($sql_date));

                    if ($date != $prev_date): ?>
                        <h4 class='concert-date'>
                            <?php 
                                secure_echo($date); 
                            ?>
                        </h4>
                    <?php $prev_date = $date; endif; ?>
                <li class='concert'>
                    <a href="<?php secure_echo($concert['url']); ?>">
                        <?php secure_echo($concert['venue']); ?> - <?php secure_echo($concert['title']); ?>
                    </a>
                </li>
            <?php
                endwhile;
            ?>
        </ul>
    </div>
</body>
</html>