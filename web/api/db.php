<?php

    $env = parse_ini_file('.env');
    $servername = $env["sql_servername"];
    $username = $env["sql_username"];
    $password = $env["sql_password"];
    $database_name = $env["sql_database"];

    // Create connection
    $conn = new mysqli($servername, $username, $password);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    /* Create database and tables if don't exist */
    // Create database
    $sql = "CREATE DATABASE IF NOT EXISTS " . $database_name;
    if ($conn->query($sql)) {

    } else {
        echo "Error creating database: " . $conn->error;
    }

    mysqli_select_db($conn, $database_name);

?>