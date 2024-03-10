<?php

function secure_echo($string) {
    if (isset($string)) {
        echo htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
    }
}

function hide_concert($conn, $title, $date, $venue, $url) {
    $stmt = $conn->prepare("UPDATE konserter SET `show`= 0 
                            WHERE title = ? AND date = ? AND venue = ? AND url = ?");
    $stmt->bind_param("ssss", $title, $date, $venue, $url);
    $status = $stmt->execute();
    if (!$status) {
        trigger_error($stmt->error, E_USER_ERROR);
    }
}

function get_latest_released_concerts($conn) {
    $sql = "SELECT title, date, venue, url, description FROM konserter
            WHERE date > DATE_SUB(NOW(), INTERVAL 1 DAY)
            ORDER BY first_seen DESC";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    $result = $stmt->get_result();
    return $result;
}

function get_concerts($conn, $q) {
    # Only return concerts that has been seen lately and filter by query if given
    $q = "%" . $q . "%";
    $sql = "SELECT title, date, venue, url, description
            FROM konserter as k1
            WHERE k1.date > DATE_SUB(NOW(), INTERVAL 1 DAY)
            AND k1.show = 1
            AND (k1.title LIKE ? OR k1.venue LIKE ?)
            AND last_seen > DATE_SUB(NOW(), INTERVAL 2 DAY)
            ORDER BY date ASC, venue";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $q, $q);
    $stmt->execute();
    $result = $stmt->get_result();
    return $result;
}

function get_venues($conn) {
    $sql = "SELECT name, up, latest_sync
            FROM venues
            ORDER BY name";
    $stmt = $conn->prepare($sql);
    $stmt->execute();
    $result = $stmt->get_result();
    return $result;
}


function concert_exists($conn, $title, $date, $venue, $url) {
    $stmt = $conn->prepare("SELECT * FROM konserter WHERE title=? AND date=? and venue=?");
    $stmt->bind_param("sss", $title, $date, $venue);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($result);

    return $stmt->num_rows > 0;
}

function create_or_update_concerts($conn, $concerts) {
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $stmt = $conn->prepare("INSERT INTO konserter (`title`, `date`, `venue`, `url`) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE `last_seen` = CURRENT_TIMESTAMP");
    $stmt->bind_param("ssss", $title, $date, $venue, $url);

    foreach ($concerts as $key => $value) {
        $title = $value->title;
        $date = $value->date;
        $venue = $value->venue;
        $url = $value->url;
        $stmt->execute();
    }
}


function create_or_update_venues($conn, $successful_venues, $failed_venues) {
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $stmt = $conn->prepare("INSERT INTO venues (`name`) VALUES (?) ON DUPLICATE KEY UPDATE `up` = 1, `latest_sync` = CURRENT_TIMESTAMP");
    $stmt->bind_param("s", $name);
    foreach ($successful_venues as $name) {
        $stmt->execute();
    }    

    $stmt = $conn->prepare("INSERT INTO venues (`name`) VALUES (?) ON DUPLICATE KEY UPDATE `up` = 0");
    $stmt->bind_param("s", $name);
    foreach ($failed_venues as $name) {
        $stmt->execute();
    }

    echo "Success";
}

?>