# Baseball Team Manager

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

A Python application for managing a baseball team roster. Track players, positions, batting stats, and calculate averages.

## Features

- Add, edit, and remove players from the roster
- Track batting statistics (at-bats, hits, batting average)
- Reorder batting lineup
- View team statistics
- Two interfaces: Console (text-based) and GUI (graphical)
- Data persistence with SQLite database and CSV backup

## Requirements

- Python 3.x
- Tkinter (included with Python)
- SQLite3 (included with Python)

## How to Run

### Console Version
```bash
python baseball_manager.py
```
This opens a text-based menu where you can manage players by typing numbered options.

### GUI Version
```bash
python player_gui.py
```
This opens a graphical window where you can load, edit, and save players using buttons and text fields.

## Project Structure

| File | Description |
|------|-------------|
| `objects.py` | Player and Lineup class definitions |
| `db.py` | Database operations (save, load, update, delete) |
| `baseball_manager.py` | Console-based interface |
| `player_gui.py` | Graphical user interface (Tkinter) |
| `ui.py` | Alternative console interface with Lineup class |
| `players.db` | SQLite database file |
| `players.csv` | CSV data file |

## Usage

### Console Menu Options
1. **Display** - Show all players in a formatted table
2. **Add** - Add a new player to the roster
3. **Remove** - Remove a player from the roster
4. **Move** - Change a player's position in the batting order
5. **Edit Pos** - Change a player's field position
6. **Edit Stats** - Update a player's at-bats and hits
7. **Stats** - View team totals and batting average
8. **Exit** - Save and quit

### Valid Positions
C, 1B, 2B, 3B, SS, LF, CF, RF, P

## Screenshots

### Console Interface
```
=============================================
BASEBALL MANAGER
=============================================
1-Display 2-Add 3-Remove 4-Move
5-Edit Pos 6-Edit Stats 7-Stats 8-Exit
=============================================
```

### GUI Interface
- Entry fields for player information
- Live batting average calculation
- Browse all players window
- Save, Cancel, Delete, and Clear buttons

## Author

Harshan Gidda
