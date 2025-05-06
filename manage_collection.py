"""
Game Collection Manager Microservice

Commands:
    python manage_collection.py

About:
    This script was created to demonstrate inter-process communication using text files
    as a simple "communication pipe" between microservices. It is part of a project
    to simulate a game collection manager where you can add, view, and remove games
    via a terminal program without any web interface.
"""

import os

PROGRAM_NAME = "Game Collection Manager Microservice"
VERSION = "v1.1"
COLLECTION_FILE = 'game_collection.txt'  # Shared text file for communication

ABOUT_TEXT = f"""
{PROGRAM_NAME} {VERSION}

This script demonstrates inter-process communication using text files as a
communication pipe between microservices. It lets you add, view, and manage (remove) games
in a shared collection. There is no web interface or database.
"""

HELP_TEXT = f"""
How to Use {PROGRAM_NAME}:

- Run this script: python manage_collection.py
- At the main menu, type a command or its number (e.g., 'view' or '1', 'add' or '2').
- To view or remove games, select 'view'/'1' at the menu.
- At the collection prompt, type:
    add     - to add a new game
    remove  - to remove a game (you'll be asked for the number)
    refresh - to reload the list
    quit    - to exit to the main menu
- Type 'quit' or '5' at any prompt to exit.
"""

def read_collection():
    """Read all games from the collection file."""
    if not os.path.exists(COLLECTION_FILE):
        return []
    with open(COLLECTION_FILE) as f:
        lines = [line.strip() for line in f if line.strip()]
    return [tuple(line.split('|')) for line in lines]

def write_collection(games):
    """Write the updated list of games back to the collection file."""
    with open(COLLECTION_FILE, 'w') as f:
        for title, genre in games:
            f.write(f"{title}|{genre}\n")

def list_games(games):
    """Display the list of games."""
    if not games:
        print("Collection is empty.")
        return
    for idx, (title, genre) in enumerate(games):
        print(f"{idx+1}. {title} ({genre})")

def remove_game(games):
    """Prompt the user to remove a game by number."""
    list_games(games)
    if not games:
        return games
    try:
        n = int(input("Enter number of game to remove (0 to cancel): "))
        if n == 0 or n > len(games):
            return games
        removed = games.pop(n-1)
        print(f'Removed "{removed[0]}" ({removed[1]}).')
    except ValueError:
        print("Invalid input.")
    return games

def add_game(games):
    """Prompt the user to add a new game."""
    print("\n[Add Game]")
    title = input("Enter game title: ").strip()
    genre = input("Enter game genre: ").strip()
    if not title or not genre:
        print("Title and genre cannot be empty.")
        return games
    games.append((title, genre))
    write_collection(games)
    print(f'Added "{title}" ({genre}) to collection.')
    return games

def manage_collection():
    """Main interface for listing, adding, and removing games."""
    while True:
        games = read_collection()
        print("\nCurrent collection:")
        list_games(games)
        print("\nCollection Commands: add | remove | refresh | quit")
        cmd = input("Command: ").strip().lower()
        if cmd in ('quit', 'q', 'exit'):
            break
        elif cmd in ('add', 'a'):
            games = add_game(games)
        elif cmd in ('remove', 'r'):
            games = remove_game(games)
            write_collection(games)
        elif cmd in ('refresh', ''):
            continue
        else:
            print("Invalid command. Type 'add', 'remove', 'refresh', or 'quit'.")

def main_menu():
    """Display the main menu and handle user choices."""
    print(f"\n{'='*40}\n{PROGRAM_NAME} {VERSION}\n{'='*40}")
    while True:
        print("\nMain Menu - enter a command or number:")
        print("  1. view     - View/manage collection")
        print("  2. add      - Add a new game")
        print("  3. about    - About this program")
        print("  4. help     - How to use")
        print("  5. quit     - Exit program")
        choice = input("Command: ").strip().lower()
        if choice in ('1', 'view', 'manage'):
            manage_collection()
        elif choice in ('2', 'add', 'a'):
            games = read_collection()
            games = add_game(games)
        elif choice in ('3', 'about'):
            print(ABOUT_TEXT)
        elif choice in ('4', 'help'):
            print(HELP_TEXT)
        elif choice in ('5', 'quit', 'exit'):
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please type 'view', 'add', 'about', 'help', 'quit' or the corresponding number.")

if __name__ == '__main__':
    main_menu()
