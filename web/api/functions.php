<?php

function secure_echo($string) {
    if (isset($string)) {
        echo htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
    }
}

function hide_concert($conn, $id) {
    $stmt = $conn->prepare("UPDATE konserter SET `show`=0 WHERE id=?");
    $stmt->bind_param("s", $id);
    $status = $stmt->execute();
    if (!$status) {
        trigger_error($stmt->error, E_USER_ERROR);
    }
}

function get_concerts($conn, $q) {
    $q = "%" . $q . "%";
    $sql = "SELECT id, title, date, venue, url, description
            FROM konserter
            WHERE date > DATE_SUB(NOW(), INTERVAL 1 DAY)
            AND `show` = 1
            AND (title LIKE ? OR venue LIKE ?)
            ORDER BY date ASC, venue";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $q, $q);
    $stmt->execute();
    $result = $stmt->get_result();
    return $result;
}

function concert_exists($conn, $title, $date, $venue, $url) {
    $stmt = $conn->prepare("SELECT id FROM konserter WHERE title=? AND date=? and venue=?");
    $stmt->bind_param("sss", $title, $date, $venue);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($result);

    return $stmt->num_rows > 0;
}

function create_concerts($conn, $concerts) {
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $stmt = $conn->prepare("INSERT INTO konserter (`title`, `date`, `venue`, `url`) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $title, $date, $venue, $url);

    foreach ($concerts as $key => $value) {
        $title = $value->title;
        $date = $value->date;
        $venue = $value->venue;
        $url = $value->url;
        if (!concert_exists($conn, $title, $date, $venue, $url)) {
            $stmt->execute();
        }
    }
}


?>