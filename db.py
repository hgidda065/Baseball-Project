# db.py
# Database and CSV helpers for persisting player data.

import csv
import sqlite3
from typing import Any, Dict, List, Optional
from objects import Player

DATABASE_PATH = "players.db"
CSV_PATH = "players.csv"
DEFAULT_POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
PLAYER_SELECT = """
    SELECT playerID, batOrder, firstName, lastName, position, atBats, hits
    FROM Player
    ORDER BY batOrder, playerID
"""


def _connect() -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _normalize_position(pos: Optional[str]) -> str:
    """Normalize position value for storage (uppercased, stripped)."""
    if pos is None:
        return ""
    return str(pos).strip().upper()


def _row_to_player(row: tuple) -> Player:
    """Convert a database row to a Player instance."""
    return Player(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


def _next_bat_order(cursor: sqlite3.Cursor) -> int:
    """Return the next batting order (max existing + 1)."""
    cursor.execute("SELECT COALESCE(MAX(batOrder), 0) + 1 FROM Player")
    return cursor.fetchone()[0]


def _ensure_position(cursor: sqlite3.Cursor, pos: Optional[str]) -> str:
    """Ensure the position exists in the Position table and return normalized value."""
    normalized = _normalize_position(pos)
    cursor.execute("INSERT OR IGNORE INTO Position(position) VALUES(?)", (normalized,))
    return normalized


def init_db() -> None:
    """Create Position and Player tables (if needed) and seed default positions."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Position (
                position TEXT PRIMARY KEY
            )
            """
        )
        cur.executemany(
            "INSERT OR IGNORE INTO Position(position) VALUES(?)",
            ((p,) for p in DEFAULT_POSITIONS),
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Player (
                playerID INTEGER PRIMARY KEY AUTOINCREMENT,
                batOrder INTEGER,
                firstName TEXT,
                lastName TEXT,
                position TEXT,
                atBats INTEGER,
                hits INTEGER,
                FOREIGN KEY(position) REFERENCES Position(position)
            )
            """
        )
        conn.commit()


def get_all() -> List[Player]:
    """Return all players sorted by batting order then playerID."""
    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(PLAYER_SELECT)
        rows = cur.fetchall()
    return [_row_to_player(r) for r in rows]


def read_all_players() -> List[Player]:
    """Alias for get_all to support alternate API naming."""
    return get_all()


def add(player: Player) -> int:
    """
    Insert a new player record and return the assigned player ID.
    If player.order is falsy, assign the next available batting order.
    """
    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        pos = _ensure_position(cur, player.pos)
        bat_order = player.order if player.order and player.order > 0 else _next_bat_order(cur)
        cur.execute(
            """
            INSERT INTO Player(batOrder, firstName, lastName, position, atBats, hits)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (bat_order, player.first, player.last, pos, player.ab, player.hits),
        )
        player.id = cur.lastrowid
        player.order = bat_order
        player.pos = pos
        conn.commit()
    return player.id


def add_player(player: Player) -> int:
    """Alias for add to support alternate API naming."""
    return add(player)


def update(player: Player) -> None:
    """Update an existing player identified by player.id."""
    if player.id is None:
        raise ValueError("player.id must be set to update a record")

    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        pos = _ensure_position(cur, player.pos)
        cur.execute(
            """
            UPDATE Player
            SET firstName = ?,
                lastName  = ?,
                position  = ?,
                atBats    = ?,
                hits      = ?
            WHERE playerID = ?
            """,
            (player.first, player.last, pos, player.ab, player.hits, player.id),
        )
        conn.commit()
    player.pos = pos


def update_player(player: Player) -> None:
    """Alias for update to support alternate API naming."""
    update(player)


def delete(player_id: int) -> None:
    """Permanently remove a player by playerID."""
    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Player WHERE playerID = ?", (player_id,))
        conn.commit()


def delete_player(player_id: int) -> None:
    """Alias for delete to support alternate API naming."""
    delete(player_id)


def update_batting_order(players: List[Player]) -> None:
    """
    Update batOrder for each player in the provided list to match list order.
    Players must have valid player.id values.
    """
    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        for idx, player in enumerate(players, start=1):
            if player.id is None:
                raise ValueError("All players must have an id to update batting order")
            cur.execute("UPDATE Player SET batOrder = ? WHERE playerID = ?", (idx, player.id))
            player.order = idx
        conn.commit()


def update_all_batting_orders(players: List[Player]) -> None:
    """Alias for update_batting_order to support alternate API naming."""
    update_batting_order(players)


def load(lineup: Any) -> None:
    """Populate the supplied Lineup object from the database."""
    lineup.players = []
    for player in get_all():
        lineup.add(player)


def save(lineup: Any) -> None:
    """
    Replace all Player rows with lineup.players.
    Batting order is set from each player's list position.
    """
    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Player")
        for idx, player in enumerate(lineup.players, start=1):
            pos = _ensure_position(cur, player.pos)
            cur.execute(
                """
                INSERT INTO Player(batOrder, firstName, lastName, position, atBats, hits)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (idx, player.first, player.last, pos, player.ab, player.hits),
            )
            player.id = cur.lastrowid
            player.order = idx
            player.pos = pos
        conn.commit()


def load_players() -> List[Dict]:
    """
    Read players from CSV with header: name,position,ab,hits.
    Returns list of dicts; malformed rows are skipped.
    """
    try:
        with open(CSV_PATH, "r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            players = []
            for row in reader:
                try:
                    players.append(
                        {
                            "name": str(row.get("name", "")).strip(),
                            "position": str(row.get("position", "")).strip(),
                            "ab": int(row.get("ab", 0)),
                            "hits": int(row.get("hits", 0)),
                        }
                    )
                except (TypeError, ValueError):
                    continue
            return players
    except FileNotFoundError:
        return []


def save_players(players: List[Dict]) -> None:
    """Write players to CSV with keys: name, position, ab, hits."""
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["name", "position", "ab", "hits"])
        writer.writeheader()
        for player in players:
            writer.writerow(
                {
                    "name": str(player.get("name", "")).replace("\n", " "),
                    "position": str(player.get("position", "")).replace("\n", " "),
                    "ab": int(player.get("ab", 0)),
                    "hits": int(player.get("hits", 0)),
                }
            )
