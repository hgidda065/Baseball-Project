import sqlite3
import csv
from objects import Player

database = "players.db"
csvfile = "players.csv"

def connect():
    conn = sqlite3.connect(database)
    return conn

def init_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Player (playerID INTEGER PRIMARY KEY AUTOINCREMENT, batOrder INTEGER, firstName TEXT, lastName TEXT, position TEXT, atBats INTEGER, hits INTEGER)")
    conn.commit()
    conn.close()

def load(lineup):
    init_db()
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player ORDER BY batOrder")
    rows = cursor.fetchall()
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Player")
    counter = 1
    for p in lineup.players:
        cursor.execute("INSERT INTO Player(batOrder,firstName,lastName,position,atBats,hits) VALUES(?,?,?,?,?,?)", (counter, p.first, p.last, p.pos, p.ab, p.hits))
        counter = counter + 1
    conn.commit()
    conn.close()

def load_players():
    try:
        player_list = []
        file = open(csvfile, 'r')
        lines = file.readlines()
        file.close()
        if len(lines) > 0:
            for i in range(1, len(lines)):
                line = lines[i]
                line = line.strip()
                parts = line.split(',')
                if len(parts) == 4:
                    player_dict = {}
                    player_dict['name'] = parts[0]
                    player_dict['position'] = parts[1]
                    player_dict['ab'] = int(parts[2])
                    player_dict['hits'] = int(parts[3])
                    player_list.append(player_dict)
        return player_list
    except:
        return []

def save_players(players):
    file = open(csvfile, 'w')
    file.write('name,position,ab,hits\n')
    for player in players:
        line = player['name'] + ',' + player['position'] + ',' + str(player['ab']) + ',' + str(player['hits']) + '\n'
        file.write(line)
    file.close()

def get_all():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player ORDER BY batOrder")
    rows = cursor.fetchall()
    player_list = []
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE Player SET firstName=?, lastName=?, position=?, atBats=?, hits=? WHERE playerID=?", (player.first, player.last, player.pos, player.ab, player.hits, player.id))
    conn.commit()
    conn.close()

def delete(player_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Player WHERE playerID=?", (player_id,))
    conn.commit()
    conn.close()
