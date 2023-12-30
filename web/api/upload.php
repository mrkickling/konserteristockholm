<?php
require "db.php";
require 'functions.php';

$env = parse_ini_file('.env');
$api_key = $_POST['api_key'];
$concerts_json = $_POST['concerts'];

if (!isset($concerts_json)) {
    die("No concerts provided\n");
}

if (!isset($api_key)) {
    die("No API Key provided\n");
}

if ($api_key != $env["API_KEY"]) {
    die("Wrong api key\n". "Should have been" . $env['API_KEY']);
}

$concerts = json_decode($concerts_json);
create_concerts($conn, $concerts);

?>