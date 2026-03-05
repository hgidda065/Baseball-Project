from objects import Player
from objects import Lineup
import db

positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P"]

def get_number(message):
    while True:
        try:
            n = int(input(message))
            if n >= 0:
                return n
            else:
                return None
        except:
            print("Invalid number")

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


def show(lineup):
    if len(lineup.players) == 0:
        print("\nNo players.\n")
        return
    print("\n#  Player               POS  AB   H    AVG")
    print("---------------------------------------------")
    for i in range(len(lineup.players)):
        p = lineup.players[i]
        player_name = p.full_name()
        player_avg = p.avg()
        spaces = 20 - len(player_name)
        spacing = ""
        for x in range(spaces):
            spacing = spacing + " "
        line = str(i+1) + "  " + player_name + spacing + p.pos + "  " + str(p.ab) + "   " + str(p.hits) + "   " + str(round(player_avg, 3))
        print(line)

def add(lineup):
    f = input("First: ")
    l = input("Last: ")
    if len(f) == 0 or len(l) == 0:
        print("Name required.")
        return
    p = get_position()
    ab = get_number("At bats: ")
    h = get_number("Hits: ")
    if h > ab:
        print("Hits > AB.")
        return
    new_player = Player(first=f, last=l, pos=p, ab=ab, hits=h)
    lineup.add(new_player)
    print("Added")

def remove(lineup):
    show(lineup)
    if len(lineup.players) == 0:
        return
    n = get_number("Remove #: ")
    if n is not None:
        if n >= 1 and n <= lineup.count():
            lineup.remove(n-1)
            print("Removed")

def move(lineup):
    show(lineup)
    if len(lineup.players) == 0:
        return
    old = get_number("Move #: ")
    new = get_number("To #: ")
    if old is not None and new is not None:
        if old >= 1 and old <= lineup.count() and new >= 1 and new <= lineup.count():
            lineup.move(old-1, new-1)
            print("Moved")

def edit_pos(lineup):
    show(lineup)
    if len(lineup.players) == 0:
        return
    n = get_number("Player #: ")
    if n is not None:
        if n >= 1 and n <= lineup.count():
            player = lineup.get(n-1)
            player.pos = get_position()
            print("Updated")

def edit_stats(lineup):
    show(lineup)
    if len(lineup.players) == 0:
        return
    n = get_number("Player #: ")
    if n is not None:
        if n >= 1 and n <= lineup.count():
            p = lineup.get(n-1)
            ab = get_number("At bats: ")
            h = get_number("Hits: ")
            if h <= ab:
                p.ab = ab
                p.hits = h
                print("Updated")
            else:
                print("Hits > AB.")

def stats(lineup):
    if len(lineup.players) == 0:
        print("\nNo players.\n")
        return
    total_ab = 0
    total_hits = 0
    for p in lineup.players:
        total_ab = total_ab + p.ab
        total_hits = total_hits + p.hits
    if total_ab > 0:
        avg = total_hits / total_ab
    else:
        avg = 0.0
    print("\nPlayers: " + str(lineup.count()))
    print("AB: " + str(total_ab))
    print("Hits: " + str(total_hits))
    print("AVG: " + str(round(avg, 3)) + "\n")

def menu():
    print("\n=============================================")
    print("BASEBALL MANAGER")
    print("=============================================")
    print("1-Display 2-Add 3-Remove 4-Move")
    print("5-Edit Pos 6-Edit Stats 7-Stats 8-Exit")
    print("=============================================")

lineup = Lineup()
db.load(lineup)
print("Loaded")

while True:
    menu()
    c = input("Choice: ")
    
    if c == "1":
        show(lineup)
    elif c == "2":
        add(lineup)
    elif c == "3":
        remove(lineup)
    elif c == "4":
        move(lineup)
    elif c == "5":
        edit_pos(lineup)
    elif c == "6":
        edit_stats(lineup)
    elif c == "7":
        stats(lineup)
    elif c == "8":
        db.save(lineup)
        print("Saved!")
        break
    else:
        print("Invalid.")
