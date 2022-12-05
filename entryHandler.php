<?php

    $json_file = 'webdata/data.json';

    // Check if there are new names to be added
    if (array_key_exists('username', $_POST)) {

        // Server parameters
        $servername = "localhost";
        $username = "vce";
        $password = "Volvo1927";
        $dbname = "vce";

        // Establish connection
        $connection = new mysqli($servername, $username, $password, $dbname);

        // TODO: Check if name already exists

        // TODO: Make sure that name is valid and not dangerous to SQL

        // Return all rows from the queue table
        $sql = "SELECT * FROM queue";
        $result = $connection->query($sql);

        // If the number of players in the queue is empty, update the json file first
        if ($result->num_rows == 0) {

            // Get and decode the data from the json file
            $json_string = file_get_contents($json_file);
            $playerInfo = json_decode($json_string, true);

            // Update the player's username
            $playerInfo['player'] = $_POST['username'];

            // Encode and put the data back into the json file
            $json_string = json_encode($playerInfo, JSON_PRETTY_PRINT);
            file_put_contents($json_file, $json_string);
        }

        // Insert new player into queue 
        //$sql = "INSERT INTO queue (username) 
        //    VALUES ('" . $_POST['username'] . "')"; // Formatting odd, had to pass as strings using '' inside of the ""
        //$connection->query($sql);
        
        $connection->close();
    }



?>