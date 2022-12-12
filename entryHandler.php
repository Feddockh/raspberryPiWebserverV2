<?php

    $json_file = 'data.json';
    $invalidLength = False;
    $explicit = False;
    $duplicate = False;

    // Check if there are new names to be added
    if (array_key_exists('username', $_POST)) {

        // Server parameters
        $servername = "localhost";
        $dbusername = "vce";
        $dbpassword = "Volvo1927";
        $dbname = "vce";

        // Establish connection
        $connection = new mysqli($servername, $dbusername, $dbpassword, $dbname);

        // Save the player's potential username
        $playerUsername = $_POST['username'];

        // Entry must be validated, begin with string length
        if (strlen($playerUsername) > 20) {
            $invalidLength = True;
            echo "Invalid Length";
        }

        // If the length is valid, check if entry is explicit
        if ($invalidLength == False) {

            // Retrieve all expletives from the expletives table in the SQL database
            $sql = "SELECT * FROM expletives";
            $result = $connection->query($sql);

            // Create an regular expression of bad words seperated by '|'
            $RegExp = "/";
            $row = $result -> fetch_array();
            $RegExp .= $row[0];
            while($row = $result -> fetch_array()) {
                $RegExp .= "|";
                $RegExp .= $row[0];
            }
            $RegExp .= "/i";

            // Try to match bad words from the regular expression to the player's username
            if (preg_match($RegExp, $playerUsername) == 1) {
                $explicit = True;
                echo "Explicit Entry";
            }
        
        }

        // If the entry length is valid and it is not explicit, then check if it already exists in the database
        if ($explicit == False) {

            // Check the queue first, then the scoreboard
            $sql = "SELECT * FROM queue WHERE username = '" . $playerUsername . "'";
            $result = $connection->query($sql);

            // Check if the number of rows exceeds 0
            if ($result->num_rows > 0) {
                $duplicate = True;
                echo "Duplicate Entry";
            }

            // If there was no duplicate in the queue then check the scoreboard
            if ($duplicate == False) {
                $sql = "SELECT * FROM scoreboard WHERE username = '" . $playerUsername . "'";
                $result = $connection->query($sql);

                // Check if the number of rows exceeds 0
                if ($result->num_rows > 0) {
                    $duplicate = True;
                    echo "Duplicate Entry";
                }
            }
        }

        // If length is valid, and entry is not explicit, and it is not a duplicate entry, then add to the database and json file
        if ($invalidLength == False && $explicit == False && $duplicate == False) {

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

            // Bind username parameter for insertion after preparing the SQL statement to protect against SQL injections
            $stmt = $connection->prepare("INSERT INTO queue (username)
                VALUES (?)");
            $stmt->bind_param("s", $_POST['username']);
            $stmt->execute();
            echo "New records created successfully";
            $stmt->close();
            
            $connection->close();
        }

    }

?>