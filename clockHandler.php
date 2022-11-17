<?php
    $output = null;
    $result_code = null;

    exec('/bin/python /var/www/html/readSerial.py', $output, $result_code);

    // Server parameters
    $servername = "localhost";
    $username = "vce";
    $password = "Volvo1927";
    $database = "vce";

    // Establish connection
    $connection = new mysqli($servername, $username, $password, $database);

    // Find the earliest entry (smallest id value)
    $sql = "SELECT MIN(id) FROM queue";
    $result = $connection->query($sql);

    if ($result->num_rows > 0) { //Check if table is empty, if not then update time in database
        $row = $result->fetch_array();
        $currentPlayerID = $row[0];

        // Update the time and the score for the row in the queue table
        $time = formatTime($output[0]);
        $score = intval($output[0]);
        $sql = "UPDATE queue SET time='" . $time . "', score=" . $score . " WHERE id = " . $currentPlayerID;
        $connection->query($sql);

        // If the output is 'END', then transfer the row from queue to the scoreboard
        if ($output[1] == 'END') {
            // Insert the row from the queue table into the scoreboard table
            $sql = "INSERT INTO scoreboard (username, time, score) SELECT username, time, score FROM queue WHERE id = " . $currentPlayerID;
            $connection->query($sql);
            
            // Delete the row from the queue table
            $sql = "DELETE FROM queue WHERE id = " . $currentPlayerID;
            $connection->query($sql);
        }

    }

    $connection->close();

    $cdTimer = formatTime(strval(300 - intval($output[0])));
    echo $cdTimer;

    // Function converts string of total seconds into timer format
    function formatTime ($strTotalSeconds) {
        $totalSeconds = intval($strTotalSeconds);
        $seconds = $totalSeconds % 60;
        $minutes = ($totalSeconds - $seconds) / 60;
        if ($seconds < 10) {
            return $minutes . ":0" . $seconds;
        } else {
            return $minutes . ":" . $seconds;
        }
    }
?>