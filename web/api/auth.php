<?php

    // Log out or authenticate as admin (password specified in .env file)
    $env = parse_ini_file('.env');
    session_start();

    if (isset($_POST['logout'])) {
        unset($_SESSION['isAdmin']);
        header('Location: ../index.php');
    }

    if (isset($_POST['password']) && isset($_POST['username'])) {
        if ($_POST['username'] == "" && $_POST['password'] == $env['admin_password']) {
            $_SESSION['isAdmin'] = True;
            header('Location: ../admin.php');
        }
    }

?>