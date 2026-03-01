from objects import Player, Lineup
import db, datetime

POS = ("C","1B","2B","3B","SS","LF","CF","RF","P")


def num(msg):
    while True:
        try:
            n = int(input(msg))
            if n < 0:
                print("Must be >=0")
            else:
                return n
        except:
            print("Invalid number.")


def pos():
    while True:
        p = input("Position: ").upper()
        if p in POS:
            return p
        print("Valid:", ", ".join(POS))


def show(lineup):
    print("\nPlayer                 POS   AB   H   AVG")
    print("-"*45)
    for i,p in enumerate(lineup,1):
        print(f"{i:<2}{p.full_name:<20}{p.pos:<5}{p.ab:<5}{p.hits:<5}{p.avg:.3f}")


def add(lineup):
    p = Player(
        input("First: "),
        input("Last: "),
        pos(),
        num("At bats: "),
        num("Hits: ")
    )
    if p.hits > p.ab:
        print("Hits cannot exceed at bats.")
        return
    lineup.add(p)
    print("Player added.")


def remove(lineup):
    show(lineup)
    i = num("Number: ")-1
    if 0 <= i < len(lineup):
        lineup.remove(i)


def move(lineup):
    show(lineup)
    o = num("Move player #: ")-1
    n = num("To position #: ")-1
    if 0<=o<len(lineup) and 0<=n<len(lineup):
        lineup.move(o,n)


def edit_pos(lineup):
    show(lineup)
    i = num("Player #: ")-1
    if 0<=i<len(lineup):
        lineup.get(i).pos = pos()


def edit_stats(lineup):
    show(lineup)
    i = num("Player #: ")-1
    if 0<=i<len(lineup):
        p = lineup.get(i)
        p.ab = num("New AB: ")
        p.hits = num("New Hits: ")


def team_stats(lineup):
    if len(lineup) == 0:
        print("No players in lineup.")
        return
    total_ab = sum(p.ab for p in lineup.players)
    total_hits = sum(p.hits for p in lineup.players)
    team_avg = total_hits / total_ab if total_ab > 0 else 0.0
    print(f"\nTeam Statistics:")
    print(f"Total Players: {len(lineup)}")
    print(f"Total At Bats: {total_ab}")
    print(f"Total Hits: {total_hits}")
    print(f"Team Batting Average: {team_avg:.3f}")


def search_player(lineup):
    name = input("Search for player name: ").lower()
    found = []
    for i,p in enumerate(lineup,1):
        if name in p.full_name.lower():
            found.append((i,p))
    if found:
        print("\nSearch Results:")
        print("Player                 POS   AB   H   AVG")
        print("-"*45)
        for i,p in found:
            print(f"{i:<2}{p.full_name:<20}{p.pos:<5}{p.ab:<5}{p.hits:<5}{p.avg:.3f}")
    else:
        print("No players found.")


def header():
    today = datetime.date.today()
    game = today + datetime.timedelta(days=2)
    print("="*60)
    print("Baseball Team Manager")
    print("CURRENT DATE:", today)
    print("GAME DATE:", game)
    print("DAYS UNTIL GAME:", (game-today).days)
    print("="*60)
    print("1 Display lineup")
    print("2 Add player")
    print("3 Remove player")
    print("4 Move player")
    print("5 Edit position")
    print("6 Edit stats")
    print("7 Team statistics")
    print("8 Search player")
    print("9 Exit")


def main():
    lineup = Lineup()
    db.load(lineup)

    while True:
        header()
        choice = input("Option: ")

        if choice=="1": show(lineup)
        elif choice=="2": add(lineup)
        elif choice=="3": remove(lineup)
        elif choice=="4": move(lineup)
        elif choice=="5": edit_pos(lineup)
        elif choice=="6": edit_stats(lineup)
        elif choice=="7": team_stats(lineup)
        elif choice=="8": search_player(lineup)
        elif choice=="9":
            db.save(lineup)
            print("Saved. Bye.")
            break
        else:
            print("Invalid option.")

main()
