# Enable extensions
import pyftdi.serialext
import mysql.connector
import json
import time

def formatTime(totalSeconds):
    seconds = totalSeconds % 60
    minutes = (totalSeconds - seconds) / 60

    if (seconds < 10):
        return "%d:0%d" % (minutes, seconds)
    else :
        return "%d:%d" % (minutes, seconds)


# Open a serial port on the FTDI device interface @ 9600 baud
port = pyftdi.serialext.serial_for_url('ftdi://ftdi:ft-x:08-15/1', baudrate=9600)

# Initialize values
second = 0
lastSecond = 0
lastPole = 0
buffer = 10
maxSeconds = 300
maxPole = 4
json_file = '/var/www/html/data.json'

# TODO: Write code to make sure that tables are set up properly

# Begin loop
while (True):

    # Receive bytes and decode into characters
    # TODO: decrease the interval of the PLC writing data to serial so that this script runs more frequently
    data = port.read(5)
    data = data.decode('UTF-8')
    data = data.split('-')
 
    # Simulation
    #time.sleep(0.5)
    #with open('/home/vce/Project/timeSim.txt') as f:
    #    data = f.read(3)

    # TODO: Make it so that SQL database is checked each cycle
        # Check to see if lowest id name matches the json file, and update it if it does not (this will allow us to skip players)
        # Pull the next up player and add them to the json file as well (also helps when skipping players)
        # Potentially absorb the tableHandler php script and put that data into the json file as well (reduces the amount of entries into the sql database since other users will now be pulling from the php file)
            # Remove table tags from the string returned by the php script and move table into index.html and then properly format table in css (fixes table size bug)
     

    # Convert string data to numerical seconds value for comparison
    second = int(data[0])
    pole = int(data[1])

    # If the second changed, then update the time (JSON)
    if (second != lastSecond or pole != lastPole):

        # Load data from the json file
        with open(json_file) as f:
            playerInfo = json.load(f)

        # Update the player's time value in the dictionary
        playerInfo["playerTime"] = formatTime(second)

        # Update the clock's time value in the dictionary
        playerInfo["clockTime"] = formatTime(maxSeconds - second)

        # Update the pole value in the dictionary
        playerInfo["pole"] = pole

        # Repackage the updated dictionary data as a json-formatted string
        json_string = json.dumps(playerInfo, indent = 4)

        # Write the json-formatted string back to our json file
        with open(json_file, 'w') as f:
            f.write(json_string)
    

    # If the game is completed, store the players time (SQL) and transfer the player from queue to the leaderboard (SQL), check for a new player and move them into the current player spot (SQL -> JSON)
    if (second == 0 and lastSecond > buffer and (lastSecond == maxSeconds or lastPole == maxPole)):
        
        # Connect to the SQL database
        dbConnection = mysql.connector.connect(
            host = "localhost",
            user = "vce",
            password = "Volvo1927",
            database = "vce"
        )

        # Create a cursor
        cursor = dbConnection.cursor()

        # Fetch the number of rows in the queue table
        query = "SELECT COUNT(*) FROM queue"
        cursor.execute(query)
        data = cursor.fetchone()
        rows = int(data[0])

        # Update and transfer the current player's info if they exist in the queue
        if (rows >= 1):

            # Find the earliest username entered into the queue
            query = "SELECT MIN(id) FROM queue"
            cursor.execute(query)
            data = cursor.fetchone()
            playerID = int(data[0])

            # TODO: Check that the username matches the one in the json file, maybe even use that username to specify the row instead of the id

            # Update the time and the score for the player
            playerTime = formatTime(lastSecond)
            playerPoles = lastPole
            playerScore = (maxSeconds - lastSecond) * 10 + playerPoles
            query = "UPDATE queue SET time = '%s', poles = %d, score = %d WHERE id = %d" % (playerTime, playerPoles, playerScore, playerID)
            cursor.execute(query)
            dbConnection.commit()

            # Copy the player's info from the queue into the leaderboard
            query = "INSERT INTO scoreboard (username, time, poles, score) SELECT username, time, poles, score FROM queue WHERE id = %d" % playerID
            cursor.execute(query)
            dbConnection.commit()
            
            # Delete the player's info from the queue
            query = "DELETE FROM queue WHERE id = %d" % playerID
            cursor.execute(query)
            dbConnection.commit()

        # Update the next player if they are in the queue
        if (rows > 1):

            # Find the next earliest username entered into the queue
            query = "SELECT username FROM queue ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            data = cursor.fetchone()
            playerUsername = data[0]
        
        # If there is no next player, then insert a blank player name
        else:
            playerUsername = ""

        # Load data from the json file
        with open(json_file) as f:
            playerInfo = json.load(f)

        # Update the username value in the dictionary
        playerInfo["player"] = playerUsername

        # Repackage the updated dictionary data as a json-formatted string
        json_string = json.dumps(playerInfo, indent = 4)

        # Write the json-formatted string back to our json file
        with open(json_file, 'w') as f:
            f.write(json_string)
        
        cursor.close()
        dbConnection.close()

    lastSecond = second
    lastPole = pole



