import sqlite3
import csv
from objects import Player

DB = "players.db"
CSV_FILE = "players.csv"

def connect():
    return sqlite3.connect(DB)

def get_all():
    with connect() as con:
        rows = con.execute(
            "SELECT * FROM Player ORDER BY batOrder"
        ).fetchall()
        return [Player(*r) for r in rows]


def add(player):
    with connect() as con:
        con.execute("""
        INSERT INTO Player(batOrder,firstName,lastName,position,atBats,hits)
        VALUES(?,?,?,?,?,?)
        """,(player.order,player.first,player.last,
             player.pos,player.ab,player.hits))


def delete(pid):
    with connect() as con:
        con.execute("DELETE FROM Player WHERE playerID=?", (pid,))


def update(player):
    with connect() as con:
        con.execute("""
        UPDATE Player
        SET firstName=?, lastName=?, position=?, atBats=?, hits=?
        WHERE playerID=?
        """,(player.first,player.last,player.pos,player.ab,player.hits,player.id))


def update_order(players):
    with connect() as con:
        for i,p in enumerate(players,1):
            con.execute(
                "UPDATE Player SET batOrder=? WHERE playerID=?",
                (i,p.id)
            )


def load_players():
    """Load players from CSV file for baseball_manager.py"""
    players = []
    try:
        with open(CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                players.append({
                    'name': row['name'],
                    'position': row['position'],
                    'ab': int(row['ab']),
                    'hits': int(row['hits'])
                })
    except FileNotFoundError:
        pass  # Return empty list if file doesn't exist
    return players


def save_players(players):
    """Save players to CSV file for baseball_manager.py"""
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'position', 'ab', 'hits'])
        writer.writeheader()
        writer.writerows(players)