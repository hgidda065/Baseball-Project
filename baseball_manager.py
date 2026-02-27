from datetime import date, datetime
from db import load_players, save_players

POSITIONS = ("C","1B","2B","3B","SS","LF","CF","RF","P")
LINE = "="*64
players = load_players()


def avg(h,ab):
    return 0.0 if ab==0 else h/ab

def show():
    if not players:
        print("No players.\n"); return
    print("\nNo Name".ljust(22),"POS AB  H   AVG")
    print("-"*64)
    for i,p in enumerate(players,1):
        print(f"{i:<2}{p['name']:<20}{p['position']:<4}{p['ab']:<4}{p['hits']:<4}{avg(p['hits'],p['ab']):.3f}")

def num(msg):
    try: return int(input(msg))
    except: print("Invalid."); return None

def pos():
    while True:
        p=input("Position: ").upper()
        if p in POSITIONS: return p
        print("Invalid position.")


def add():
    name=input("Name: ")
    p=pos()
    while True:
        ab=num("AB: "); h=num("Hits: ")
        if ab is None or h is None: continue
        if ab<0 or h<0 or h>ab: print("Invalid stats.")
        else: break
    players.append({"name":name,"position":p,"ab":ab,"hits":h})

def remove():
    show(); n=num("Remove #: ")
    if n and 1<=n<=len(players): players.pop(n-1)

def move():
    show()
    a=num("Move #: "); b=num("New #: ")
    if a and b and 1<=a<=len(players) and 1<=b<=len(players):
        players.insert(b-1, players.pop(a-1))

def edit_pos():
    show(); n=num("Player #: ")
    if n and 1<=n<=len(players): players[n-1]["position"]=pos()

def edit_stats():
    show(); n=num("Player #: ")
    if not n or not 1<=n<=len(players): return
    while True:
        ab=num("AB: "); h=num("Hits: ")
        if ab is None or h is None: continue
        if ab<0 or h<0 or h>ab: print("Invalid.")
        else: break
    players[n-1]["ab"],players[n-1]["hits"]=ab,h


today=date.today()
print(LINE,"\nBaseball Team Manager".center(64),"\n"+LINE)
print("CURRENT DATE:",today)

d=input("Next game date YYYY-MM-DD: ").strip()
if d:
    try:
        g=datetime.strptime(d,"%Y-%m-%d").date()
        if g>today: print("DAYS UNTIL GAME:",(g-today).days)
    except: print("Invalid date.")

print("\nPOSITIONS:",", ".join(POSITIONS))
print(LINE)


while True:
    print("\n1 Display  2 Add  3 Remove  4 Move  5 Edit Pos  6 Edit Stats  7 Exit")
    c=input("Choice: ")

    if c=="1": show()
    elif c=="2": add()
    elif c=="3": remove()
    elif c=="4": move()
    elif c=="5": edit_pos()
    elif c=="6": edit_stats()
    elif c=="7":
        save_players(players)
        print("Saved. Bye!")
        break
    else:
        print("Invalid option.")
