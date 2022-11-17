<?php
    // Server parameters
    $servername = "localhost";
    $username = "vce";
    $password = "Volvo1927";
    $dbname = "vce";

    // Establish connection
    $connection = new mysqli($servername, $username, $password, $dbname);

    // Check if there are new names to be added
    if (array_key_exists('username', $_POST)) {

        // TODO: Check if name already exists
        
        // Insert data into table
        $sql = "INSERT INTO queue (username, time) 
            VALUES ('" . $_POST['username'] . "', '" . '0:00' . "')"; // Formatting odd, had to pass as strings using '' inside of the ""
        $connection->query($sql);
    }
?>