<?php
    // Server parameters
    $servername = "localhost";
    $username = "vce";
    $password = "Volvo1927";

    // Establish connection
    $connection = new mysqli($servername, $username, $password);

    // Validate connection
    if ($conection->connect_error) {
        die ("Connection failed: " . $connection->connect_error) . "<br>";
    } else {
        echo "Connected succesfully<br>";
    }

    // Create a database
    $sql = "CREATE DATABASE IF NOT EXISTS vce";
    if ($connection->query($sql) == TRUE) {
        echo "Database created successfully<br>";
    } else {
        echo "Error creating database: " . $connection->error . "<br>";
    }

    $connection->close();

    // Create a new connection in database
    $dbname = "vce";
    $connection = new mysqli($servername, $username, $password, $dbname);
    if ($conection->connect_error) {
        die ("Connection failed: " . $connection->connect_error) . "<br>";
    } else {
        echo "Connected succesfully<br>";
    }

    // Create a table for queue
    $sql = "CREATE OR REPLACE TABLE queue (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(30) NOT NULL,
        time VARCHAR(10),
        poles INT(1),
        score INT(6)
        )";
    if ($connection->query($sql) == TRUE) {
        echo "Table created successfully<br>";
    } else {
        echo "Error creating table: " . $connection->error . "<br>";
    }

    /*
    // Create a table for scoreboard
    $sql = "CREATE OR REPLACE TABLE scoreboard (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(30) NOT NULL,
        time VARCHAR(10),
        poles INT(1),
        score INT(6)
        )";
    if ($connection->query($sql) == TRUE) {
        echo "Table created successfully<br>";
    } else {
        echo "Error creating table: " . $connection->error . "<br>";
    }
    */

    $connection->close();
?>