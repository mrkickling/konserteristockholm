<?php
require "db.php";
require 'functions.php';

$env = parse_ini_file('.env');
$api_key = $_POST['api_key'];
$concerts_json = $_POST['concerts'];
$successful_venues_json = $_POST['successful_venues'];
$failed_venues_json = $_POST['failed_venues'];

if (!isset($concerts_json)) {
    die("No concerts provided\n");
}

if (!isset($successful_venues_json) && !isset($failed_venues_json)) {
    die("No venues provided\n");
}

if (!isset($api_key)) {
    die("No API Key provided\n");
}

if ($api_key != $env["API_KEY"]) {
    die("Wrong api key");
}

$concerts = json_decode($concerts_json);
$successful_venues = json_decode($successful_venues_json, true);
$failed_venues = json_decode($failed_venues_json, true);

if (!$failed_venues) {
    $failed_venues = [];
}
if (!$successful_venues) {
    $successful_venues = [];
}

create_or_update_concerts($conn, $concerts);
create_or_update_venues($conn, $successful_venues, $failed_venues);

?>