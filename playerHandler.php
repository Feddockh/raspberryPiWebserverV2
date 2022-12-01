<?php
    // Server parameters
    $servername = "localhost";
    $username = "vce";
    $password = "Volvo1927";
    $database = "vce";

    // Establish connection
    $connection = new mysqli($servername, $username, $password, $database);

    $sql = "SELECT username, time FROM queue ORDER BY id ASC LIMIT 1";
    $result = $connection->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_array();

        /*
        $table = "
            <table>
                <tr>
                    <td>" . $row["username"] . "</td>
                    <td>" . $row["time"] . "</td>
                </tr>
        ";

        echo $table;
        */
        echo $row["username"] . " " . $row["time"];
    }

    $connection->close();

?>