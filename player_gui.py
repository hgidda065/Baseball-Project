import tkinter as tk
from tkinter import messagebox
import db
from objects import Player

current_player = None

db.init_db()

def clear():
    global current_player
    current_player = None
    id_entry.delete(0, tk.END)
    for e in entries.values():
        e.delete(0, tk.END)
        e.config(bg="white")
    avg_var.set("")

def load_player():
    global current_player
    pid = id_entry.get()

    if not pid.isdigit():
        messagebox.showerror("Error","Invalid ID")
        return

    players = db.get_all()
    for p in players:
        if str(p.id) == pid:
            current_player = p
            fill_fields(p)
            return

    messagebox.showerror("Error","Player not found")

def fill_fields(p):
    entries["first"].delete(0, tk.END)
    entries["first"].insert(0, p.first)

    entries["last"].delete(0, tk.END)
    entries["last"].insert(0, p.last)

    entries["pos"].delete(0, tk.END)
    entries["pos"].insert(0, p.pos)

    entries["ab"].delete(0, tk.END)
    entries["ab"].insert(0, p.ab)

    entries["hits"].delete(0, tk.END)
    entries["hits"].insert(0, p.hits)

    average = p.avg()
    avg_var.set(str(round(average, 3)))

def calculate_avg():
    try:
        ab = int(entries["ab"].get())
        hits = int(entries["hits"].get())
        if hits > ab:
            entries["hits"].config(bg="#ffcccc")
            avg_var.set("ERR")
        else:
            entries["hits"].config(bg="white")
            entries["ab"].config(bg="white")
            if ab > 0:
                avg = hits / ab
            else:
                avg = 0.0
            avg_var.set(str(round(avg, 3)))
    except:
        avg_var.set("---")

def save():
    global current_player
    if not current_player:
        messagebox.showwarning("Warning", "No player loaded")
        return

    try:
        first = entries["first"].get().strip()
        last = entries["last"].get().strip()
        pos = entries["pos"].get().strip()
        ab = int(entries["ab"].get())
        hits = int(entries["hits"].get())
        if not first or not last:
            messagebox.showerror("Error", "Name required")
            return
        if hits > ab or ab < 0 or hits < 0:
            messagebox.showerror("Error", "Invalid stats")
            return
        current_player.first = first
        current_player.last = last
        current_player.pos = pos
        current_player.ab = ab
        current_player.hits = hits
    except ValueError:
        messagebox.showerror("Error","Invalid numbers")
        return
    db.update(current_player)
    messagebox.showinfo("Saved","Player updated")
    clear()

def cancel():
    if current_player:
        fill_fields(current_player)
    else:
        clear()

def delete_player():
    global current_player
    if not current_player:
        messagebox.showwarning("Warning", "No player loaded")
        return
    player_name = current_player.full_name()
    confirm = messagebox.askyesno("Delete", "Delete " + player_name + "?")
    if confirm:
        db.delete(current_player.id)
        messagebox.showinfo("Deleted", "Player deleted")
        clear()

def show_all_players():
    players = db.get_all()
    if not players:
        messagebox.showinfo("No Players", "Database is empty")
        return
    browse_win = tk.Toplevel(root)
    browse_win.title("All Players")
    browse_win.geometry("400x280")
    listbox = tk.Listbox(browse_win, font=("Courier", 10), width=50, height=12)
    listbox.pack(padx=10, pady=10)
    for p in players:
        player_name = p.full_name()
        player_avg = p.avg()
        line = "ID:" + str(p.id) + " | " + player_name + " | " + p.pos + " | AVG: " + str(round(player_avg, 3))
        listbox.insert(tk.END, line)
    def load_selected():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            player = players[index]
            id_entry.delete(0, tk.END)
            id_entry.insert(0, player.id)
            browse_win.destroy()
            load_player()
    def on_double_click(event):
        load_selected()
    btn_frame = tk.Frame(browse_win)
    btn_frame.pack(pady=5)
    load_btn = tk.Button(btn_frame, text="Load", command=load_selected, width=10)
    load_btn.pack(side=tk.LEFT, padx=5)
    close_btn = tk.Button(btn_frame, text="Close", command=browse_win.destroy, width=10)
    close_btn.pack(side=tk.LEFT, padx=5)
    listbox.bind('<Double-Button-1>', on_double_click)

root = tk.Tk()
root.title("Baseball Player Editor")
root.geometry("450x350")

labels = ["Player ID", "First name", "Last name", "Position", "At bats", "Hits", "Batting Avg"]
for i in range(len(labels)):
    label = tk.Label(root, text=labels[i])
    label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

get_btn = tk.Button(root, text="Get Player", command=load_player)
get_btn.grid(row=0, column=2, padx=5)

entries = {}
keys = ["first", "last", "pos", "ab", "hits"]
for i in range(len(keys)):
    e = tk.Entry(root)
    e.grid(row=i+1, column=1)
    entries[keys[i]] = e

def on_ab_change(event):
    calculate_avg()

def on_hits_change(event):
    calculate_avg()
entries["ab"].bind("<KeyRelease>", on_ab_change)
entries["hits"].bind("<KeyRelease>", on_hits_change)

avg_var = tk.StringVar()
avg_entry = tk.Entry(root, textvariable=avg_var, state="readonly")
avg_entry.grid(row=6, column=1)

button_frame = tk.Frame(root)
button_frame.grid(row=7, column=0, columnspan=3, pady=10)

save_btn = tk.Button(button_frame, text="Save", command=save, bg="#90EE90", width=10)
save_btn.pack(side=tk.LEFT, padx=5)

cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel, width=10)
cancel_btn.pack(side=tk.LEFT, padx=5)

delete_btn = tk.Button(button_frame, text="Delete", command=delete_player, bg="#FFB6C6", width=10)
delete_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(button_frame, text="Clear", command=clear, width=10)
clear_btn.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(root, text="Browse All Players", command=show_all_players, bg="#ADD8E6", width=25)
browse_btn.grid(row=8, column=0, columnspan=3, pady=10)

def on_ctrl_s(event):
    save()

def on_escape(event):
    cancel()

root.bind('<Control-s>', on_ctrl_s)
root.bind('<Escape>', on_escape)
root.mainloop()