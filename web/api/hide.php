<?php

// Hide a specific concert / event
session_start();
require 'db.php';
require 'functions.php';

if (isset(($_POST['id']))) {
    $id = $_POST['id'];
    if (isset($_SESSION['isAdmin']) && $_SESSION['isAdmin']) {
        hide_concert($conn, $id);
        header('Location: ../index.php');
    }
}
?>