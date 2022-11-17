<?php
    // Server parameters
    $servername = "localhost";
    $username = "vce";
    $password = "Volvo1927";
    $database = "vce";

    // Establish connection
    $connection = new mysqli($servername, $username, $password, $database);

    // ORDER BY clause used to sort records in ascending order
    $sql = "SELECT username, time, score FROM scoreboard ORDER BY score ASC LIMIT 10";
    $result = $connection->query($sql);

    // Begin the table by setting the headers for each column
    if ($result->num_rows > 0) {
        $table = "
            <table border = 1> 
                <tr>
                    <th> Rank </th>
                    <th> Username </th>
                    <th> Time </th>
                </tr>
        ";

        // Increment through each row and add the data under its respective header
        $i = 1;
        while ($row = $result->fetch_array()) {
            $table .= "
                <tr>
                    <td>" . $i . "</td>
                    <td>" . $row["username"] . "</td>
                    <td>" . $row["time"] . "</td>
                </tr>
            ";
            $i++;
        }

        // Close the table and print it
        $table .= "</table";
        echo $table;
    }

    // Close database connection
    $connection->close();
?>