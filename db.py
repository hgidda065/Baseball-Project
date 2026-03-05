# db.py - Database operations for player data persistence
# Handles SQLite database and CSV file operations

import sqlite3
import csv
from objects import Player

# File paths for data storage
database = "players.db"  # SQLite database file
csvfile = "players.csv"  # CSV backup file

def connect():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(database)
    return conn

def init_db():
    """
    Initializes the database by creating the Player table if it doesn't exist.
    Called at startup to ensure the database schema is ready.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Player (playerID INTEGER PRIMARY KEY AUTOINCREMENT, batOrder INTEGER, firstName TEXT, lastName TEXT, position TEXT, atBats INTEGER, hits INTEGER)")
    conn.commit()
    conn.close()

def load(lineup):
    """
    Loads all players from the database into the provided Lineup object.
    Players are sorted by their batting order position.
    """
    init_db()
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player ORDER BY batOrder")
    rows = cursor.fetchall()
    # Convert each database row into a Player object
    for row in rows:
        player_id = row[0]
        bat_order = row[1]
        first_name = row[2]
        last_name = row[3]
        position = row[4]
        at_bats = row[5]
        hits = row[6]
        p = Player(player_id, bat_order, first_name, last_name, position, at_bats, hits)
        lineup.add(p)
    conn.close()

def save(lineup):
    """
    Saves the entire lineup to the database.
    Clears existing data and inserts all players with updated batting order.
    """
    conn = connect()
    cursor = conn.cursor()
    # Clear existing players - we'll re-insert with current order
    cursor.execute("DELETE FROM Player")
    counter = 1
    for p in lineup.players:
        cursor.execute("INSERT INTO Player(batOrder,firstName,lastName,position,atBats,hits) VALUES(?,?,?,?,?,?)", (counter, p.first, p.last, p.pos, p.ab, p.hits))
        counter = counter + 1
    conn.commit()
    conn.close()

def load_players():
    """
    Loads player data from the CSV file.
    Returns a list of player dictionaries.
    Used as an alternative to database storage.
    """
    try:
        player_list = []
        file = open(csvfile, 'r')
        lines = file.readlines()
        file.close()
        # Skip header line (index 0) and process data rows
        if len(lines) > 0:
            for i in range(1, len(lines)):
                line = lines[i]
                line = line.strip()
                parts = line.split(',')
                # Validate that we have all 4 expected fields
                if len(parts) == 4:
                    player_dict = {}
                    player_dict['name'] = parts[0]
                    player_dict['position'] = parts[1]
                    player_dict['ab'] = int(parts[2])
                    player_dict['hits'] = int(parts[3])
                    player_list.append(player_dict)
        return player_list
    except:
        # Return empty list if file doesn't exist or has errors
        return []

def save_players(players):
    """
    Saves player data to the CSV file.
    Creates a header row followed by one row per player.
    """
    file = open(csvfile, 'w')
    file.write('name,position,ab,hits\n')  # CSV header
    for player in players:
        line = player['name'] + ',' + player['position'] + ',' + str(player['ab']) + ',' + str(player['hits']) + '\n'
        file.write(line)
    file.close()

def get_all():
    """
    Retrieves all players from the database.
    Returns a list of Player objects sorted by batting order.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player ORDER BY batOrder")
    rows = cursor.fetchall()
    player_list = []
    # Convert database rows to Player objects
    for row in rows:
        player_id = row[0]
        bat_order = row[1]
        first_name = row[2]
        last_name = row[3]
        position = row[4]
        at_bats = row[5]
        hits = row[6]
        p = Player(player_id, bat_order, first_name, last_name, position, at_bats, hits)
        player_list.append(p)
    conn.close()
    return player_list

def update(player):
    """
    Updates an existing player record in the database.
    Uses the player's ID to identify which record to update.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE Player SET firstName=?, lastName=?, position=?, atBats=?, hits=? WHERE playerID=?", (player.first, player.last, player.pos, player.ab, player.hits, player.id))
    conn.commit()
    conn.close()

def delete(player_id):
    """
    Removes a player from the database by their ID.
    This action is permanent and cannot be undone.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Player WHERE playerID=?", (player_id,))
    conn.commit()
    conn.close()
