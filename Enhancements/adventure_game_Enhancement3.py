# Create by Tyler Pimental
# CS-499
# An adventure game where you navigate between rooms of a fantasy world.

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import sqlite3
import time

# Database setup
db_connection = sqlite3.connect("high_scores.db")
db_cursor = db_connection.cursor()

# Create the high scores table if it doesn't exist
db_cursor.execute("""
CREATE TABLE IF NOT EXISTS high_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time REAL NOT NULL
)
""")
db_connection.commit()

# Game timer and items
start_time = None
items_collected = set()

# Define the rooms, their connections, and image file paths
# Each room has interactable regions to allow the player to navigate to other rooms

rooms = {
    "Hall": { 
        "description": "You are in a grand hall. There are doors to the kitchen and library.", # The description to display to the user
        "middle_left": "Kitchen",   # the variable defines the region the user will have to click, the value is the destination
        "top_right": "Library",
        "image": "images/hall.png", # The asset to use for the room
        "assigned_regions": ["middle_left", "top_right"], # This is used for debugging purposes, to draw the regions
        "items": {"bottom_center": {"name": "Candle", "collected": False}} # Define items found within the room

    },
    "Library": {
        "description": "You are in a quiet library filled with books. There's a door back to the hall.",
        "bottom_center": "Hall",
        "image": "images/library.png",
        "assigned_regions": ["bottom_center"],
        "items": {"top_left": {"name": "Wand", "collected": False}}
    },
    "Kitchen": {
        "description": "You are in a cozy kitchen. There are doors to the hall and garden.",
        "top_left": "Hall",
        "bottom_center": "Garden",
        "image": "images/kitchen.png",
        "assigned_regions": ["top_left", "bottom_center"],
        "items": {"middle_center": {"name": "Whisk", "collected": False}}
    },
    "Garden": {
        "description": "You are in a beautiful garden. There's a door back to the kitchen.",
        "top_center": "Kitchen",
        "image": "images/garden.png",
        "assigned_regions": ["top_center"],
        "items": {"bottom_right": {"name": "Gnome Statue", "collected": False}}
    }
}

# Game timer and items
start_time = None
items_collected = set()

def start_timer():
    global start_time
    start_time = time.time()

def stop_timer():
    if start_time:
        return time.time() - start_time
    return None

def check_completion():
    # Check if all items are collected
    all_items = {item["name"] for room in rooms.values() for item in room.get("items", {}).values()}
    if items_collected == all_items:
        end_time = stop_timer()
        if end_time is not None:
            player_name = get_player_name(end_time)
            if player_name:
                save_high_score(player_name, end_time)
                display_high_scores()

def get_player_name(score_time):
    # Prompt player to input name
    return simpledialog.askstring("Game Completed!", f"Congratulations! You completed the game in {score_time:.2f} seconds.\nEnter your name:")

def save_high_score(name, score_time):
    # Save high score to the database
    db_cursor.execute("INSERT INTO high_scores (name, time) VALUES (?, ?)", (name, score_time))
    db_connection.commit()

def display_high_scores():
    # Retrieve and display top 10 high scores
    db_cursor.execute("SELECT name, time FROM high_scores ORDER BY time ASC LIMIT 10")
    scores = db_cursor.fetchall()
    high_scores = "\n".join([f"{i+1}. {name}: {score_time:.2f}s" for i, (name, score_time) in enumerate(scores)])
    messagebox.showinfo("High Scores", f"Top 10 High Scores:\n\n{high_scores}")

# Dynamically calulate the regions based on the size of the game window
# The regions are a 3x3 grid built as a dictionary
def calculate_regions(window_width, window_height):
    third_width = window_width // 3
    third_height = window_height // 3

    return {
        "top_left": (0, 0, third_width, third_height),
        "top_center": (third_width, 0, 2 * third_width, third_height),
        "top_right": (2 * third_width, 0, window_width, third_height),
        
        "middle_left": (0, third_height, third_width, 2 * third_height),
        "middle_center": (third_width, third_height, 2 * third_width, 2 * third_height),
        "middle_right": (2 * third_width, third_height, window_width, 2 * third_height),
        
        "bottom_left": (0, 2 * third_height, third_width, window_height),
        "bottom_center": (third_width, 2 * third_height, 2 * third_width, window_height),
        "bottom_right": (2 * third_width, 2 * third_height, window_width, window_height)
    }

# Function to update the room description and image
def update_display():
    global room_image
    room = rooms[current_room]
    room_description.set(f"Current Room: {current_room}\n\n{room['description']}")
    
    # Load the image for the current room
    img = Image.open(room['image'])
    img = img.resize((640, 480), Image.Resampling.LANCZOS)
    room_image = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_container, image=room_image)

    # For debugging, display regions
    # First clear old regions
    canvas.delete("region")
    # In red, display the location of room regions
    regions = calculate_regions(640, 480)  # Use the image size for regions
    for region_name in room["assigned_regions"]:
        left, top, right, bottom = regions[region_name]
        canvas.create_rectangle(left, top, right, bottom, outline="red", width=2, tags="region")
    # In blue, show the locations of item regions
    for region_name, item in room.get("items", {}).items():
        if not item["collected"]:  # Only draw if the item is not collected
            left, top, right, bottom = regions[region_name]
            canvas.create_rectangle(left, top, right, bottom, outline="blue", width=2, tags="region")

# Function to handle mouse clicks on the canvas
def handle_click(x, y, current_room, window_width, window_height):
    regions = calculate_regions(window_width, window_height)
    room_data = rooms[current_room]

    # Check for item clicks
    for region_name, item in room_data.get("items", {}).items():
        if not item["collected"]:  # Only check for uncollected items
            left, top, right, bottom = regions[region_name]
            if left <= x <= right and top <= y <= bottom: # Determine if the click was within bounds of the region
                item["collected"] = True
                items_collected.add(item["name"])
                update_display()  # Redraw the room to hide the item region
                check_completion()  # Check if the game is completed
                return None  # Do not change the room

    # Check for room navigation clicks
    for region_name in room_data["assigned_regions"]:
        left, top, right, bottom = regions[region_name]
        if left <= x <= right and top <= y <= bottom: # Determine if the click was within bounds of the region
            return room_data.get(region_name)

    return None # If the user did not click a region, return nothing!


# Set the default room for the player
current_room = "Hall"

# Detect user input from their mouse
def on_canvas_click(event):
    global current_room
    window_width = canvas.winfo_width()
    window_height = canvas.winfo_height()
    new_room = handle_click(event.x, event.y, current_room, window_width, window_height)
    
    if new_room:
        current_room = new_room
        update_room()
    else:
        print("There's nothing here!")

def update_room():
    update_display();

def load_room_image(room):
    image_path = rooms[room]["image"]
    image = Image.open(image_path)
    image = image.resize((640, 480), Image.Resampling.LANCZOS) # Static values here for now, TO DO: make this re-sizable by the player
    tk_image = ImageTk.PhotoImage(image)
    return tk_image

start_timer()

# Initialize the tkinter window
root = tk.Tk()
root.title("Text-Based Adventure Game")

room_description = tk.StringVar()
room_description.set("Welcome to the game!")  # Initial message or placeholder

# Create the canvas and image container
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()
image_container = canvas.create_image(0, 0, anchor=tk.NW)

# Bind mouse click events
canvas.bind("<Button-1>", on_canvas_click)

# Initialize the display
update_display()

# Begin execution
root.mainloop()

db_connection.close()