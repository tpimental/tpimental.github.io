# Create by Tyler Pimental
# CS-499
# An adventure game where you navigate between rooms of a fantasy world.

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Define the rooms, their connections, and image file paths
# Each room has interactable regions to allow the player to navigate to other rooms

rooms = {
    "Hall": { 
        "description": "You are in a grand hall. There are doors to the kitchen and library.",
        "middle_left": "Kitchen",
        "top_right": "Library",
        "image": "images/hall.png",
        "assigned_regions": ["middle_left", "top_right"]
    },
    "Library": {
        "description": "You are in a quiet library filled with books. There's a door back to the hall.",
        "bottom_center": "Hall",
        "image": "images/library.png",
        "assigned_regions": ["bottom_center"]
    },
    "Kitchen": {
        "description": "You are in a cozy kitchen. There are doors to the hall and garden.",
        "top_left": "Hall",
        "bottom_center": "Garden",
        "image": "images/kitchen.png",
        "assigned_regions": ["top_left", "bottom_center"]
    },
    "Garden": {
        "description": "You are in a beautiful garden. There's a door back to the kitchen.",
        "top_center": "Kitchen",
        "image": "images/garden.png",
        "assigned_regions": ["top_center"]
    }
}

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
    img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
    room_image = ImageTk.PhotoImage(img)
    canvas.itemconfig(image_container, image=room_image)

# Function to handle mouse clicks on the canvas
def handle_click(x, y, current_room, window_width, window_height):

    regions = calculate_regions(window_width, window_height)
    room_data = rooms[current_room]
    
    for region_name in room_data["assigned_regions"]:
        coords = regions[region_name]
        left, top, right, bottom = coords
        if left <= x <= right and top <= y <= bottom:
            return room_data.get(region_name)
    
    return None

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
    room = rooms[current_room]
    print(room["description"])
    tk_image = load_room_image(current_room)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.image = tk_image  # Store reference to prevent garbage collection

def load_room_image(room):
    image_path = rooms[room]["image"]
    image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(image)
    return tk_image

# Initialize the tkinter window
root = tk.Tk()
root.title("Text-Based Adventure Game")

tk_image = load_room_image(current_room)
canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
canvas.bind("<Button-1>", on_canvas_click)

update_room()
root.mainloop()