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
    </div>
</body>
</html>

