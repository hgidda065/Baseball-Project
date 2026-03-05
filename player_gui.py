# player_gui.py - Graphical interface for editing baseball players
# Built with tkinter for a user-friendly editing experience

import tkinter as tk
from tkinter import messagebox
import db
from objects import Player

# Currently loaded player for editing (None if no player loaded)
current_player = None

# Make sure database table exists before we start
db.init_db()

def clear():
    """Clears all form fields and resets to initial state."""
    global current_player
    current_player = None
    id_entry.delete(0, tk.END)
    # Clear all input fields
    for e in entries.values():
        e.delete(0, tk.END)
        e.config(bg="white")
    avg_var.set("")

def load_player():
    """Loads a player from database by ID and fills the form."""
    global current_player
    pid = id_entry.get()

    # Validate that ID is a number
    if not pid.isdigit():
        messagebox.showerror("Error","Invalid ID")
        return

    # Search for player with matching ID
    players = db.get_all()
    for p in players:
        if str(p.id) == pid:
            current_player = p
            fill_fields(p)
            return

    messagebox.showerror("Error","Player not found")

def fill_fields(p):
    """Populates form fields with player data."""
    # Fill each text field with player info
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

    # Calculate and display batting average
    average = p.avg()
    avg_var.set(str(round(average, 3)))

def calculate_avg():
    """
    Calculates batting average in real-time as user types.
    Shows error if hits exceeds at bats.
    """
    try:
        ab = int(entries["ab"].get())
        hits = int(entries["hits"].get())
        # Highlight error if hits > at bats
        if hits > ab:
            entries["hits"].config(bg="#ffcccc")  # Red background
            avg_var.set("ERR")
        else:
            # Reset backgrounds and calculate
            entries["hits"].config(bg="white")
            entries["ab"].config(bg="white")
            if ab > 0:
                avg = hits / ab
            else:
                avg = 0.0
            avg_var.set(str(round(avg, 3)))
    except:
        # Show placeholder if fields are empty or invalid
        avg_var.set("---")

def save():
    """Saves current player changes to the database."""
    global current_player
    if not current_player:
        messagebox.showwarning("Warning", "No player loaded")
        return

    try:
        # Get values from form fields
        first = entries["first"].get().strip()
        last = entries["last"].get().strip()
        pos = entries["pos"].get().strip()
        ab = int(entries["ab"].get())
        hits = int(entries["hits"].get())
        # Validate required fields
        if not first or not last:
            messagebox.showerror("Error", "Name required")
            return
        # Validate stat values
        if hits > ab or ab < 0 or hits < 0:
            messagebox.showerror("Error", "Invalid stats")
            return
        # Update player object with form values
        current_player.first = first
        current_player.last = last
        current_player.pos = pos
        current_player.ab = ab
        current_player.hits = hits
    except ValueError:
        messagebox.showerror("Error","Invalid numbers")
        return
    # Save to database and confirm
    db.update(current_player)
    messagebox.showinfo("Saved","Player updated")
    clear()

def cancel():
    """Reverts form to last saved state or clears if no player loaded."""
    if current_player:
        fill_fields(current_player)
    else:
        clear()

def delete_player():
    """Removes the current player from the database after confirmation."""
    global current_player
    if not current_player:
        messagebox.showwarning("Warning", "No player loaded")
        return
    # Ask for confirmation before deleting
    player_name = current_player.full_name()
    confirm = messagebox.askyesno("Delete", "Delete " + player_name + "?")
    if confirm:
        db.delete(current_player.id)
        messagebox.showinfo("Deleted", "Player deleted")
        clear()

def show_all_players():
    """Opens a popup window listing all players for selection."""
    players = db.get_all()
    if not players:
        messagebox.showinfo("No Players", "Database is empty")
        return
    # Create popup window
    browse_win = tk.Toplevel(root)
    browse_win.title("All Players")
    browse_win.geometry("400x280")
    # Create listbox to display all players
    listbox = tk.Listbox(browse_win, font=("Courier", 10), width=50, height=12)
    listbox.pack(padx=10, pady=10)
    # Add each player to the listbox
    for p in players:
        player_name = p.full_name()
        player_avg = p.avg()
        line = "ID:" + str(p.id) + " | " + player_name + " | " + p.pos + " | AVG: " + str(round(player_avg, 3))
        listbox.insert(tk.END, line)
    def load_selected():
        """Loads the selected player into the main form."""
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            player = players[index]
            id_entry.delete(0, tk.END)
            id_entry.insert(0, player.id)
            browse_win.destroy()
            load_player()
    def on_double_click(event):
        """Handle double-click to load player."""
        load_selected()
    # Add buttons at bottom of popup
    btn_frame = tk.Frame(browse_win)
    btn_frame.pack(pady=5)
    load_btn = tk.Button(btn_frame, text="Load", command=load_selected, width=10)
    load_btn.pack(side=tk.LEFT, padx=5)
    close_btn = tk.Button(btn_frame, text="Close", command=browse_win.destroy, width=10)
    close_btn.pack(side=tk.LEFT, padx=5)
    # Enable double-click to load
    listbox.bind('<Double-Button-1>', on_double_click)

# === MAIN WINDOW SETUP ===
root = tk.Tk()
root.title("Baseball Player Editor")
root.geometry("450x350")

# Create labels for each form field
labels = ["Player ID", "First name", "Last name", "Position", "At bats", "Hits", "Batting Avg"]
for i in range(len(labels)):
    label = tk.Label(root, text=labels[i])
    label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

# Player ID input with Get button
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

get_btn = tk.Button(root, text="Get Player", command=load_player)
get_btn.grid(row=0, column=2, padx=5)

# Create entry fields for player data
entries = {}
keys = ["first", "last", "pos", "ab", "hits"]
for i in range(len(keys)):
    e = tk.Entry(root)
    e.grid(row=i+1, column=1)
    entries[keys[i]] = e

# Event handlers for live average calculation
def on_ab_change(event):
    calculate_avg()

def on_hits_change(event):
    calculate_avg()

# Bind key events to update average in real-time
entries["ab"].bind("<KeyRelease>", on_ab_change)
entries["hits"].bind("<KeyRelease>", on_hits_change)

# Read-only field for calculated batting average
avg_var = tk.StringVar()
avg_entry = tk.Entry(root, textvariable=avg_var, state="readonly")
avg_entry.grid(row=6, column=1)

# === BUTTON SECTION ===
button_frame = tk.Frame(root)
button_frame.grid(row=7, column=0, columnspan=3, pady=10)

# Save button - green color for positive action
save_btn = tk.Button(button_frame, text="Save", command=save, bg="#90EE90", width=10)
save_btn.pack(side=tk.LEFT, padx=5)

# Cancel button - reverts changes
cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel, width=10)
cancel_btn.pack(side=tk.LEFT, padx=5)

# Delete button - pink color for warning
delete_btn = tk.Button(button_frame, text="Delete", command=delete_player, bg="#FFB6C6", width=10)
delete_btn.pack(side=tk.LEFT, padx=5)

# Clear button - resets form
clear_btn = tk.Button(button_frame, text="Clear", command=clear, width=10)
clear_btn.pack(side=tk.LEFT, padx=5)

# Browse button - opens player list popup
browse_btn = tk.Button(root, text="Browse All Players", command=show_all_players, bg="#ADD8E6", width=25)
browse_btn.grid(row=8, column=0, columnspan=3, pady=10)

# === KEYBOARD SHORTCUTS ===
def on_ctrl_s(event):
    """Save shortcut handler."""
    save()

def on_escape(event):
    """Escape key handler."""
    cancel()

# Bind keyboard shortcuts for power users
root.bind('<Control-s>', on_ctrl_s)
root.bind('<Escape>', on_escape)

# Start the application
root.mainloop()