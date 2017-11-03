<?php
    //check_login_details.php
    $uid = $_POST['usn'];
    $psw = $_POST['psw'];
    
    if (strlen($uid) > 10) {
        echo "Okay";
    }
    else {
        echo "Nope";
    }

?>
