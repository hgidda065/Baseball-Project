# db.py
# Database and CSV helpers for persisting player data.

import csv
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from objects import Player

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = str(BASE_DIR / "players.db")
CSV_PATH = str(BASE_DIR / "players.csv")
DEFAULT_POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
PLAYER_SELECT = """
    SELECT playerID, batOrder, firstName, lastName, position, atBats, hits
    FROM Player
    ORDER BY batOrder, playerID
"""


def _connect() -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH, timeout=30)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
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


def _split_name(name: str) -> tuple[str, str]:
    """Split full name into first and last name parts."""
    cleaned = str(name).strip()
    if not cleaned:
        return "", ""
    parts = cleaned.split(maxsplit=1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


def _seed_players_from_csv_if_empty(cursor: sqlite3.Cursor) -> int:
    """Import CSV players into Player table only when the table is empty."""
    cursor.execute("SELECT COUNT(*) FROM Player")
    if cursor.fetchone()[0] > 0:
        return 0

    seeded = 0
    for idx, raw in enumerate(load_players(), start=1):
        first, last = _split_name(raw.get("name", ""))
        pos = _ensure_position(cursor, raw.get("position", ""))

        try:
            ab = int(raw.get("ab", 0))
        except (TypeError, ValueError):
            ab = 0

        try:
            hits = int(raw.get("hits", 0))
        except (TypeError, ValueError):
            hits = 0

        ab = max(0, ab)
        hits = max(0, min(hits, ab))

        cursor.execute(
            """
            INSERT INTO Player(batOrder, firstName, lastName, position, atBats, hits)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (idx, first, last, pos, ab, hits),
        )
        seeded += 1

    return seeded


def init_db() -> None:
    """Create Position and Player tables (if needed) and seed default positions."""
    with _connect() as conn:
        cur = conn.cursor()

        # Create schema if missing.
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Player'")
        has_player_table = cur.fetchone() is not None
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Position'")
        has_position_table = cur.fetchone() is not None
        if not has_position_table:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS Position (
                    position TEXT PRIMARY KEY
                )
                """
            )
        if not has_player_table:
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

        cur.execute("SELECT COUNT(*) FROM Position")
        position_count = cur.fetchone()[0]
        if position_count == 0:
            cur.executemany(
                "INSERT OR IGNORE INTO Position(position) VALUES(?)",
                ((p,) for p in DEFAULT_POSITIONS),
            )

        _seed_players_from_csv_if_empty(cur)

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
    """Write players to CSV and synchronize the SQLite Player table."""
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

    # Keep GUI and console apps in sync by reflecting CSV changes into SQLite.
    init_db()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Player")
        for idx, raw in enumerate(players, start=1):
            first, last = _split_name(raw.get("name", ""))
            pos = _ensure_position(cur, raw.get("position", ""))

            try:
                ab = int(raw.get("ab", 0))
            except (TypeError, ValueError):
                ab = 0

            try:
                hits = int(raw.get("hits", 0))
            except (TypeError, ValueError):
                hits = 0

            ab = max(0, ab)
            hits = max(0, min(hits, ab))

            cur.execute(
                """
                INSERT INTO Player(batOrder, firstName, lastName, position, atBats, hits)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (idx, first, last, pos, ab, hits),
            )

        conn.commit()
