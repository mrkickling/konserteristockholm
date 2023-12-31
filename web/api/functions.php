<?php

function secure_echo($string) {
    echo htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

function get_all_concerts($conn) {
    $sql = "SELECT * FROM konserter WHERE date > DATE_SUB(NOW(), INTERVAL 1 DAY) ORDER BY date ASC";
    $result = $conn->query($sql);
    return $result;
}

function concert_exists($conn, $title, $date, $venue, $url) {
    $stmt = $conn->prepare("SELECT id FROM konserter WHERE title=? AND date=? and venue=?");
    $stmt->bind_param("ssss", $title, $date, $venue, $url);
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