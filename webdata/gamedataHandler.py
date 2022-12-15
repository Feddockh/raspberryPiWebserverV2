# Enable extensions
import pyftdi.serialext
import mysql.connector
import json

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

# Setup the json file for use
# Dictionary with json format for setup
json_file_format = {'player': '', 'playerTime': '0:00', 'clockTime': '5:00', 'pole': 0, 'nextPlayer': '', 'scoreboard': {'1': {'username': 'brian', 'time': '0:27', 'poles': 4}, '2': {'username': 'bart', 'time': '0:29', 'poles': 4}, '3': {'username': 'filip', 'time': '0:55', 'poles': 4}, '4': {'username': 'Just Tony', 'time': '0:58', 'poles': 4}, '5': {'username': 'shovelman', 'time': '2:39', 'poles': 4}, '6': {'username': 'joe', 'time': '2:41', 'poles': 4}, '7': {'username': 'rudgehoist', 'time': '4:14', 'poles': 4}, '8': {'username': 'Brajovic Harness Company', 'time': '5:00', 'poles': 2}, '9': {'username': 'checking', 'time': '5:00', 'poles': 0}, '10': {'username': '', 'time': '', 'poles': ''}}}

# Repackage the setup dictionary data as a json-formatted string
json_string = json.dumps(json_file_format, indent = 4)

# Write the json-formatted setup string to our json file
with open(json_file, 'w') as f:
    f.write(json_string)


# TODO: Write code to make sure that tables are set up properly

# Begin loop
while (True):

    # Receive bytes and decode into characters
    # TODO: decrease the interval of the PLC writing data to serial so that this script runs more frequently
    # TODO: Implement 'END' feature
    data = port.read(5)
    data = data.decode('UTF-8')
    data = data.split('-')


    # Check for shutdown
    if (data[0] == 'OFF'):
        break

    
    # Convert string data to numerical seconds value for comparison
    second = int(data[0])
    pole = int(data[1])


    # Load in the data from the json file
    with open(json_file) as f:
        playerInfo = json.load(f)


    # If the second changed, then update the time (JSON)
    if (second != lastSecond or pole != lastPole):

        # Update the player's time value in the dictionary
        playerInfo["playerTime"] = formatTime(second)

        # Update the clock's time value in the dictionary
        playerInfo["clockTime"] = formatTime(maxSeconds - second)

        # Update the pole value in the dictionary
        playerInfo["pole"] = pole


    # Connect to the SQL database
    dbConnection = mysql.connector.connect(
        host = "localhost",
        user = "vce",
        password = "Volvo1927",
        database = "vce"
    )

    # Create a cursor
    cursor = dbConnection.cursor()

    # Update the scoreboard
    # Fetch the top 10 ranked players, and their stats, from the scoreboard
    query = "SELECT username, time, poles, score FROM scoreboard ORDER BY score DESC LIMIT 10"
    cursor.execute(query)
    data = cursor.fetchall()

    # Iterate through the top 10 rows from the json file while inserting data from the SQL database
    i = 1
    for x in data:
        playerInfo["scoreboard"][str(i)]["username"] = x[0]
        playerInfo["scoreboard"][str(i)]["time"] = x[1]
        playerInfo["scoreboard"][str(i)]["poles"] = x[2]
        i = i + 1

    # If there are less than 10 players in the scoreboard, then fill the additional rows with blank data
    while (i <= 10):
        playerInfo["scoreboard"][str(i)]["username"] = ""
        playerInfo["scoreboard"][str(i)]["time"] = ""
        playerInfo["scoreboard"][str(i)]["poles"] = ""
        i = i + 1


    # Fetch the number of rows in the queue table
    query = "SELECT COUNT(*) FROM queue"
    cursor.execute(query)
    data = cursor.fetchone()
    rows = int(data[0])

    # If there are rows in the table then update the username of the current and next player
    if (rows >= 1):

        # Find the 2 earliest usernames entered into the queue
        query = "SELECT username FROM queue ORDER BY id ASC LIMIT 2"
        cursor.execute(query)
        data = cursor.fetchall()

        # Find the username of the current player in the json file
        playerUsername = str(data[0])
        playerUsername = playerUsername.strip("('',)")

        # Find the username of the next player in the json file (if there is one)
        if (rows >= 2):
            nextPlayerUsername = str(data[1])
            nextPlayerUsername = nextPlayerUsername.strip("('',)")
        else:
            nextPlayerUsername = ""

    # If the are no rows, and the game is running, then set the username to 'error'
    elif (rows == 0 and second > 0):

        # Return error to display on screen
        playerUsername = "ERR: NO_PLAYER"
        nextPlayerUsername = ""

    # If there are no rows in the table update the username to be blank
    else:
        
        # Blank player names
        playerUsername = ""
        nextPlayerUsername = ""

    # Update the current and next player's usernames
    playerInfo["player"] = playerUsername
    playerInfo["nextPlayer"] = nextPlayerUsername

    # Repackage the updated dictionary data as a json-formatted string
    json_string = json.dumps(playerInfo, indent = 4)

    # Write the json-formatted string back to our json file
    with open(json_file, 'w') as f:
        f.write(json_string)


    # If the game is completed, store the players time (SQL) and transfer the player from queue to the leaderboard (SQL), check for a new player and move them into the current player spot (SQL -> JSON)
    if (second == 0 and lastSecond > buffer and (lastSecond == maxSeconds or lastPole == maxPole)):
      
        # Update and transfer the current player's info if they exist in the queue
        if (rows >= 1):

            # TODO: Complete with username instead of min id?

            # Fetch the number of rows in the queue table
            query = "SELECT MIN(id) FROM queue"
            cursor.execute(query)
            data = cursor.fetchone()
            playerID = int(data[0])

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
    
    cursor.close()
    dbConnection.close()

    lastSecond = second
    lastPole = pole

exit(0)



