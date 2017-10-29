<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width-device-width, initial-scale = 1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="hh_style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
    <link href='https://fonts.googleapis.com/css?family=Alegreya' rel='stylesheet'>
    <script scr="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/jk/bootstrap.min.js"></script>

</head>
<body>

<div class="container" id="confirm">
    <div class="jumbotron" align="center">
        <h1 class="display-3" id="confirm">
            <?php
            $word = $_GET["first-name"];
            echo "Thank you " + $first-name "for using Flyt";
            ?>
        </h1>
        <p>Please check your phone for a confirmation</p>
    </div>
    
    <?php
    $myObj->address = $_GET["address"];
    $myObj->number = $_GET["number"];
    $myObj->trans = $_GET["trans"];
    $myObj->airport = $_GET["airport"];
    $myObj->flyid = $_GET["flyid"];
    $myObj->departTime = $_GET["departure"];

    $myJSON = json_encode($myObj);

    //echo $myJSON;
    ?>
</div>


</body>
</html>
