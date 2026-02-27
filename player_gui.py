import tkinter as tk
from tkinter import messagebox
import db
from objects import Player

current_player = None



def clear():
    for e in entries.values():
        e.delete(0, tk.END)

def load_player():
    global current_player
    pid = id_entry.get()

    if not pid.isdigit():
        messagebox.showerror("Error","Invalid ID")
        clear()
        return

    players = db.get_all()
    for p in players:
        if str(p.id) == pid:
            current_player = p
            fill_fields(p)
            return

    messagebox.showerror("Error","Player not found")
    clear()

def fill_fields(p):
    entries["first"].delete(0,tk.END)
    entries["first"].insert(0,p.first)

    entries["last"].delete(0,tk.END)
    entries["last"].insert(0,p.last)

    entries["pos"].delete(0,tk.END)
    entries["pos"].insert(0,p.pos)

    entries["ab"].delete(0,tk.END)
    entries["ab"].insert(0,p.ab)

    entries["hits"].delete(0,tk.END)
    entries["hits"].insert(0,p.hits)

    avg_var.set(f"{p.avg:.3f}")

def save():
    global current_player
    if not current_player:
        return

    try:
        current_player.first = entries["first"].get()
        current_player.last = entries["last"].get()
        current_player.pos = entries["pos"].get()
        current_player.ab = int(entries["ab"].get())
        current_player.hits = int(entries["hits"].get())
    except:
        messagebox.showerror("Error","Invalid numbers")
        return

    db.update(current_player)
    messagebox.showinfo("Saved","Player updated")
    clear()

def cancel():
    if current_player:
        fill_fields(current_player)

# ---------- window ----------

root = tk.Tk()
root.title("Player Editor")

labels = ["Player ID","First name","Last name","Position","At bats","Hits","Batting Avg"]

for i,l in enumerate(labels):
    tk.Label(root,text=l).grid(row=i,column=0,sticky="e",padx=5,pady=5)

id_entry = tk.Entry(root)
id_entry.grid(row=0,column=1)

tk.Button(root,text="Get Player",command=load_player)\
.grid(row=0,column=2,padx=5)

entries = {}
keys = ["first","last","pos","ab","hits"]

for i,k in enumerate(keys,1):
    e = tk.Entry(root)
    e.grid(row=i,column=1)
    entries[k]=e

avg_var = tk.StringVar()
tk.Entry(root,textvariable=avg_var,state="readonly")\
.grid(row=6,column=1)

# buttons
tk.Button(root,text="Save Changes",command=save)\
.grid(row=7,column=0,pady=10)

tk.Button(root,text="Cancel",command=cancel)\
.grid(row=7,column=1)

root.mainloop()