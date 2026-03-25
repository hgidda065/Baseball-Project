# player_gui.py
# Graphical interface for editing baseball players using tkinter.

import tkinter as tk
from tkinter import messagebox
import db
from objects import Player

# Currently loaded player for editing. None if no player is loaded.
current_player = None

# Make sure database table exists before UI starts
db.init_db()


def clear():
    """Clear all form fields and reset the editing state."""
    global current_player
    current_player = None
    id_entry.delete(0, tk.END)

    for e in entries.values():
        e.delete(0, tk.END)
        e.config(bg="white")

    avg_var.set("---")


def fill_fields(p):
    """Populate the form fields from a Player object."""
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

    # Show batting average (formatted to three decimals)
    try:
        avg = p.avg()
        avg_var.set(f"{avg:.3f}")
    except Exception:
        avg_var.set("---")


def load_player():
    """Load a player by ID from the database and fill the form."""
    global current_player
    pid = id_entry.get().strip()

    if not pid.isdigit():
        messagebox.showerror("Error", "Invalid ID")
        return

    players = db.get_all()
    if not players:
        messagebox.showinfo("No Players", "No players found. Add players first, then try again.")
        return

    for p in players:
        if str(p.id) == pid:
            current_player = p
            fill_fields(p)
            return

    # Fallback: users often type lineup order number (1..N) instead of DB playerID.
    # Players are already sorted by batting order in db.get_all().
    index = int(pid) - 1
    if 0 <= index < len(players):
        current_player = players[index]
        id_entry.delete(0, tk.END)
        id_entry.insert(0, str(current_player.id))
        fill_fields(current_player)
        return

    messagebox.showerror("Error", "Player not found")


def calculate_avg():
    """
    Recompute batting average from the form fields.
    If inputs are invalid or empty, show a placeholder.
    """
    try:
        ab_text = entries["ab"].get().strip()
        hits_text = entries["hits"].get().strip()

        if ab_text == "" or hits_text == "":
            avg_var.set("---")
            entries["ab"].config(bg="white")
            entries["hits"].config(bg="white")
            return

        ab = int(ab_text)
        hits = int(hits_text)

        if ab < 0 or hits < 0:
            avg_var.set("ERR")
            return

        if hits > ab:
            entries["hits"].config(bg="#ffcccc")
            avg_var.set("ERR")
            return

        entries["hits"].config(bg="white")
        entries["ab"].config(bg="white")
        avg = (hits / ab) if ab > 0 else 0.0
        avg_var.set(f"{avg:.3f}")

    except ValueError:
        # Non-integer values while typing
        avg_var.set("---")


def save():
    """Save changes for the currently loaded player back into the database."""
    global current_player
    if not current_player:
        messagebox.showwarning("Warning", "No player loaded")
        return

    first = entries["first"].get().strip()
    last = entries["last"].get().strip()
    pos = entries["pos"].get().strip()

    try:
        ab = int(entries["ab"].get().strip())
        hits = int(entries["hits"].get().strip())
    except ValueError:
        messagebox.showerror("Error", "Invalid numbers")
        return

    if not first or not last:
        messagebox.showerror("Error", "Name required")
        return

    if ab < 0 or hits < 0 or hits > ab:
        messagebox.showerror("Error", "Invalid stats")
        return

    # Update object and persist
    current_player.first = first
    current_player.last = last
    current_player.pos = pos
    current_player.ab = ab
    current_player.hits = hits

    db.update(current_player)
    messagebox.showinfo("Saved", "Player updated")
    clear()


def cancel():
    """Restore the last loaded player's values or clear if none loaded."""
    if current_player:
        fill_fields(current_player)
    else:
        clear()


def delete_player():
    """Delete the currently loaded player after user confirmation."""
    global current_player
    if not current_player:
        messagebox.showwarning("Warning", "No player loaded")
        return

    player_name = current_player.full_name()
    confirm = messagebox.askyesno("Delete", f"Delete {player_name}?")
    if confirm:
        db.delete(current_player.id)
        messagebox.showinfo("Deleted", "Player deleted")
        clear()


def show_all_players():
    """Open a popup listing all players; allow user to load one."""
    players = db.get_all()
    if not players:
        messagebox.showinfo("No Players", "Database is empty")
        return

    browse_win = tk.Toplevel(root)
    browse_win.title("All Players")
    browse_win.geometry("420x300")

    listbox = tk.Listbox(browse_win, font=("Courier", 10), width=60, height=12)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for p in players:
        player_name = p.full_name()
        player_avg = p.avg()
        line = f"ID:{p.id:3} | {player_name:20} | {p.pos:3} | AVG: {player_avg:.3f}"
        listbox.insert(tk.END, line)

    def load_selected():
        sel = listbox.curselection()
        if not sel:
            return
        index = sel[0]
        player = players[index]
        id_entry.delete(0, tk.END)
        id_entry.insert(0, player.id)
        browse_win.destroy()
        load_player()

    btn_frame = tk.Frame(browse_win)
    btn_frame.pack(pady=5)

    load_btn = tk.Button(btn_frame, text="Load", command=load_selected, width=10)
    load_btn.pack(side=tk.LEFT, padx=5)
    close_btn = tk.Button(btn_frame, text="Close", command=browse_win.destroy, width=10)
    close_btn.pack(side=tk.LEFT, padx=5)

    listbox.bind('<Double-Button-1>', lambda e: load_selected())


# === MAIN WINDOW SETUP ===
root = tk.Tk()
root.title("Baseball Player Editor")
root.geometry("480x360")

labels = ["Player ID", "First name", "Last name", "Position", "At bats", "Hits", "Batting Avg"]
for i, text in enumerate(labels):
    label = tk.Label(root, text=text)
    label.grid(row=i, column=0, sticky="e", padx=6, pady=6)

# Player ID entry and Get button
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, sticky="we", padx=6)

get_btn = tk.Button(root, text="Get Player", command=load_player, width=12)
get_btn.grid(row=0, column=2, padx=6)

# Create entry fields for player data
entries = {}
keys = ["first", "last", "pos", "ab", "hits"]
for i, key in enumerate(keys, start=1):
    e = tk.Entry(root)
    e.grid(row=i, column=1, sticky="we", padx=6)
    entries[key] = e

# Bind key events to update average in real-time
def on_ab_change(event):
    calculate_avg()

def on_hits_change(event):
    calculate_avg()

entries["ab"].bind("<KeyRelease>", on_ab_change)
entries["hits"].bind("<KeyRelease>", on_hits_change)

# Read-only field for batting average
avg_var = tk.StringVar(value="---")
avg_entry = tk.Entry(root, textvariable=avg_var, state="readonly")
avg_entry.grid(row=6, column=1, sticky="we", padx=6)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=7, column=0, columnspan=3, pady=12)

save_btn = tk.Button(button_frame, text="Save", command=save, bg="#90EE90", width=10)
save_btn.pack(side=tk.LEFT, padx=6)

cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel, width=10)
cancel_btn.pack(side=tk.LEFT, padx=6)

delete_btn = tk.Button(button_frame, text="Delete", command=delete_player, bg="#FFB6C6", width=10)
delete_btn.pack(side=tk.LEFT, padx=6)

clear_btn = tk.Button(button_frame, text="Clear", command=clear, width=10)
clear_btn.pack(side=tk.LEFT, padx=6)

browse_btn = tk.Button(root, text="Browse All Players", command=show_all_players, bg="#ADD8E6", width=30)
browse_btn.grid(row=8, column=0, columnspan=3, pady=8)

# Keyboard shortcuts
def on_ctrl_s(event):
    save()

def on_escape(event):
    cancel()

root.bind('<Control-s>', on_ctrl_s)
root.bind('<Escape>', on_escape)

# Start the application
root.mainloop()
