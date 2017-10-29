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
                echo ("Thank you ". $name ." for using Flyt");
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
    $myObj = new StdClass;
    $myObj->address = $_GET["addr"];
    $myObj->number = $_GET["num"];
    $myObj->trans = $_GET["trans"];
    $myObj->airport = $_GET["air"];
    $myObj->flightId = $_GET["flyid"];
    $myObj->selfCheck = $_GET["self"];
    $myObj->departTime = strtotime(str_replace("T", " ", $_GET["departure"]));

    $content = json_encode($myObj);

    $url = "http://127.0.0.1:5000/";    
    

    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_HEADER, false);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER,
            array("Content-type: application/json"));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $content);

    $json_response = curl_exec($curl);

    $status = curl_getinfo($curl, CURLINFO_HTTP_CODE);

    if ( $status != 201 ) {
        die("Error: call to URL $url failed with status $status, response $json_response, curl_error " . curl_error($curl) . ", curl_errno " . curl_errno($curl));
    }


    curl_close($curl);

    $response = json_decode($json_response, true);

    //echo $myJSON;
    ?>
</div>


</body>
</html>
