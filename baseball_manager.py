# baseball_manager.py - Console-based baseball team manager
# Allows users to manage players through a text menu interface

from db import load_players, save_players

# Valid baseball positions: Catcher, bases, shortstop, outfield, pitcher
positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P"]

# Load existing players from CSV file at startup
players = load_players()

def calculate_avg(hits, at_bats):
    """Calculates batting average, returns 0 if no at bats."""
    if at_bats == 0:
        return 0.0
    else:
        return hits / at_bats

def get_number(message):
    """Prompts for an integer input, returns None if invalid."""
    try:
        value = int(input(message))
        return value
    except:
        print("Invalid number")
        return None

def get_position():
    """
    Prompts for a valid baseball position.
    Keeps asking until user enters a valid position code.
    """
    while True:
        p = input("Position: ")
        p = p.upper()  # Accept lowercase input
        # Check if entered position is in our valid list
        valid = False
        for position in positions:
            if p == position:
                valid = True
                break
        if valid:
            return p
        print("Invalid position")


def show():
    """Displays all players in a formatted table with stats."""
    if len(players) == 0:
        print("\nNo players\n")
        return
    # Print table header
    print("\n")
    print("#    Name                 POS  AB   H    AVG")
    print("---------------------------------------------")
    # Print each player's info
    for i in range(len(players)):
        p = players[i]
        player_avg = calculate_avg(p['hits'], p['ab'])
        # Add padding to align columns
        spaces = 20 - len(p['name'])
        spacing = ""
        for x in range(spaces):
            spacing = spacing + " "
        line = str(i+1) + "    " + p['name'] + spacing + p['position'] + "   " + str(p['ab']) + "   " + str(p['hits']) + "   " + str(round(player_avg, 3))
        print(line)

def add():
    """Adds a new player to the roster."""
    n = input("Name: ")
    if len(n) == 0:
        print("Name required")
        return
    p = get_position()
    a = get_number("AB: ")
    h = get_number("Hits: ")
    # Validate input values
    if a is None or h is None:
        print("Invalid")
        return
    # Check for logical errors in stats
    if a < 0 or h < 0 or h > a:
        print("Invalid stats")
        return
    # Create player dictionary and add to list
    new_player = {'name': n, 'position': p, 'ab': a, 'hits': h}
    players.append(new_player)
    print("Added")

def remove():
    """Removes a player from the roster by their lineup number."""
    show()
    if len(players) == 0:
        return
    n = get_number("Remove #: ")
    # Validate selection is in valid range
    if n is not None:
        if n >= 1 and n <= len(players):
            players.pop(n-1)  # Convert to 0-based index
            print("Removed")

def move():
    """Moves a player to a different position in the batting order."""
    show()
    if len(players) == 0:
        return
    f = get_number("Move #: ")
    t = get_number("To #: ")
    # Validate both positions are valid
    if f is not None and t is not None:
        if f >= 1 and f <= len(players) and t >= 1 and t <= len(players):
            # Remove from old position and insert at new position
            player = players.pop(f-1)
            players.insert(t-1, player)
            print("Moved")

def edit_pos():
    """Changes a player's field position."""
    show()
    if len(players) == 0:
        return
    n = get_number("Player #: ")
    if n is not None:
        if n >= 1 and n <= len(players):
            players[n-1]['position'] = get_position()
            print("Updated")

def edit_stats():
    """Updates a player's batting statistics."""
    show()
    if len(players) == 0:
        return
    n = get_number("Player #: ")
    if n is None:
        return
    if n < 1 or n > len(players):
        return
    a = get_number("AB: ")
    h = get_number("Hits: ")
    # Validate stats are numbers
    if a is None or h is None:
        print("Invalid")
        return
    # Validate stats are logical (can't have more hits than at bats)
    if a < 0 or h < 0 or h > a:
        print("Invalid stats")
        return
    players[n-1]['ab'] = a
    players[n-1]['hits'] = h
    print("Updated")

def stats():
    """Displays team-wide statistics summary."""
    if len(players) == 0:
        print("\nNo players\n")
        return
    # Calculate totals across all players
    total_ab = 0
    total_hits = 0
    for p in players:
        total_ab = total_ab + p['ab']
        total_hits = total_hits + p['hits']
    team_avg = calculate_avg(total_hits, total_ab)
    # Display team summary
    print("\nPlayers: " + str(len(players)))
    print("AB: " + str(total_ab))
    print("Hits: " + str(total_hits))
    print("AVG: " + str(round(team_avg, 3)) + "\n")


# === MAIN PROGRAM ===
# Display welcome message and load count
print("\n=============================================")
print("BASEBALL MANAGER")
print("=============================================")
print("Loaded " + str(len(players)) + " players")

# Main menu loop - runs until user chooses to exit
while True:
    # Display menu options
    print("\n=============================================")
    print("1-Display 2-Add 3-Remove 4-Move")
    print("5-Edit Pos 6-Edit Stats 7-Stats 8-Exit")
    print("=============================================")
    c = input("Choice: ")
    
    # Handle menu selection
    if c == "1":
        show()
    elif c == "2":
        add()
    elif c == "3":
        remove()
    elif c == "4":
        move()
    elif c == "5":
        edit_pos()
    elif c == "6":
        edit_stats()
    elif c == "7":
        stats()
    elif c == "8":
        # Save data and exit
        save_players(players)
        print("Saved!")
        break
    else:
        print("Invalid")
