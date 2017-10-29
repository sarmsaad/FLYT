<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width-device-width, initial-scale = 1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="style2.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
    <link href='https://fonts.googleapis.com/css?family=Alegreya' rel='stylesheet'>
    <script scr="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/jk/bootstrap.min.js"></script>
    <link href='https://fonts.googleapis.com/css?family=Lobster' rel='stylesheet'>

</head>
<body>

<div class="container" id="confirm">
    <div class="jumbotron" align="center">
        <h1 class="display-3" id="confirm">
            <?php
            $name = $_GET["first-name"];
            if (is_null($name)){
                echo "Thank you for using Flyt";
            }
            else{
                echo ("Thank you, ". $name ." for using Flyt");
            }
            ?>
        </h1>
        <p>Please check your phone for a confirmation</p>
        <h2>Have a safe flight</h2>
        <p class="lead">
                <a class="btn btn-primary btn-lg" href="flyt.html" role="button">Try Again</a>
        </p>
    </div>

    <?php

    $myObj->address = $_GET["addr"];
    $myObj->number = $_GET["num"];
    $myObj->trans = $_GET["transport"];
    $myObj->airport = $_GET["air"];
    $myObj->flightId = $_GET["flyid"];
    $myObj->selfCheck = $_GET["#self"]
    $myObj->departTime = str_replace("T", " ", $_GET["departure"]);

    $myJSON = json_encode($myObj);

    //echo $myJSON;
    ?>
</div>


</body>
</html>
