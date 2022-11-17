<?php
    $output = null;
    $result_code = null;

    exec('/bin/python /var/www/html/readSerial.py', $output, $result_code);
    
    echo $output[0];
?>