from db import load_players, save_players

positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P"]
players = load_players()

def calculate_avg(hits, at_bats):
    if at_bats == 0:
        return 0.0
    else:
        return hits / at_bats

def get_number(message):
    try:
        value = int(input(message))
        return value
    except:
        print("Invalid number")
        return None

def get_position():
    while True:
        p = input("Position: ")
        p = p.upper()
        valid = False
        for position in positions:
            if p == position:
                valid = True
                break
        if valid:
            return p
        print("Invalid position")


def show():
    if len(players) == 0:
        print("\nNo players\n")
        return
    print("\n")
    print("#    Name                 POS  AB   H    AVG")
    print("---------------------------------------------")
    for i in range(len(players)):
        p = players[i]
        player_avg = calculate_avg(p['hits'], p['ab'])
        spaces = 20 - len(p['name'])
        spacing = ""
        for x in range(spaces):
            spacing = spacing + " "
        line = str(i+1) + "    " + p['name'] + spacing + p['position'] + "   " + str(p['ab']) + "   " + str(p['hits']) + "   " + str(round(player_avg, 3))
        print(line)

def add():
    n = input("Name: ")
    if len(n) == 0:
        print("Name required")
        return
    p = get_position()
    a = get_number("AB: ")
    h = get_number("Hits: ")
    if a is None or h is None:
        print("Invalid")
        return
    if a < 0 or h < 0 or h > a:
        print("Invalid stats")
        return
    new_player = {'name': n, 'position': p, 'ab': a, 'hits': h}
    players.append(new_player)
    print("Added")

def remove():
    show()
    if len(players) == 0:
        return
    n = get_number("Remove #: ")
    if n is not None:
        if n >= 1 and n <= len(players):
            players.pop(n-1)
            print("Removed")

def move():
    show()
    if len(players) == 0:
        return
    f = get_number("Move #: ")
    t = get_number("To #: ")
    if f is not None and t is not None:
        if f >= 1 and f <= len(players) and t >= 1 and t <= len(players):
            player = players.pop(f-1)
            players.insert(t-1, player)
            print("Moved")

def edit_pos():
    show()
    if len(players) == 0:
        return
    n = get_number("Player #: ")
    if n is not None:
        if n >= 1 and n <= len(players):
            players[n-1]['position'] = get_position()
            print("Updated")

def edit_stats():
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
    if a is None or h is None:
        print("Invalid")
        return
    if a < 0 or h < 0 or h > a:
        print("Invalid stats")
        return
    players[n-1]['ab'] = a
    players[n-1]['hits'] = h
    print("Updated")

def stats():
    if len(players) == 0:
        print("\nNo players\n")
        return
    total_ab = 0
    total_hits = 0
    for p in players:
        total_ab = total_ab + p['ab']
        total_hits = total_hits + p['hits']
    team_avg = calculate_avg(total_hits, total_ab)
    print("\nPlayers: " + str(len(players)))
    print("AB: " + str(total_ab))
    print("Hits: " + str(total_hits))
    print("AVG: " + str(round(team_avg, 3)) + "\n")


print("\n=============================================")
print("BASEBALL MANAGER")
print("=============================================")
print("Loaded " + str(len(players)) + " players")

while True:
    print("\n=============================================")
    print("1-Display 2-Add 3-Remove 4-Move")
    print("5-Edit Pos 6-Edit Stats 7-Stats 8-Exit")
    print("=============================================")
    c = input("Choice: ")
    
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
        save_players(players)
        print("Saved!")
        break
    else:
        print("Invalid")
