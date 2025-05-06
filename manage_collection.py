import os

PROGRAM_NAME = "Game Collection Manager Microservice"
VERSION = "v1.2"
TAGLINE = "Manage your game collection and wishlist instantly, privately, and for free."

COLLECTION_FILE = 'game_collection.txt'
WISHLIST_FILE = 'wishlist.txt'

ABOUT_TEXT = f"""
{PROGRAM_NAME} {VERSION}

This script demonstrates inter-process communication using text files as a
communication pipe between microservices. It lets you add, view, and manage (remove) games
in a shared collection or wishlist. There are no advertisements, subscriptions, or monetary 
costs—this program is completely free.
"""

HELP_TEXT = f"""
How to Use {PROGRAM_NAME}:

- Run this script: python manage_collection.py
- At the main menu, type a command or its number (e.g., 'view' or '1', 'wishlist' or '6').
- Use commands 'add', 'remove', 'refresh', and 'quit' within collection or wishlist views.
"""

### Shared Utilities ###

def read_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]
    return [tuple(line.split('|')) for line in lines]

def write_file(filename, games):
    with open(filename, 'w') as f:
        for title, genre in games:
            f.write(f"{title}|{genre}\n")

def list_games(games, label="Game"):
    if not games:
        print(f"{label} list is empty.")
        return
    for idx, (title, genre) in enumerate(games):
        print(f"{idx+1}. {title} ({genre})")

def remove_game(games, label="game"):
    list_games(games, label=label.capitalize())
    if not games:
        return games
    try:
        n = int(input(f"Enter number of {label} to remove (0 to cancel): "))
        if n == 0 or n > len(games):
            return games
        removed = games.pop(n-1)
        print(f'Removed "{removed[0]}" ({removed[1]}).')
    except ValueError:
        print("Invalid input.")
    return games

def add_game(games, label="game"):
    print(f"\n[Add {label.capitalize()}]")
    title = input("Enter title: ").strip()
    genre = input("Enter genre: ").strip()
    if not title or not genre:
        print("Title and genre cannot be empty.")
        return games
    games.append((title, genre))
    print(f'Added "{title}" ({genre}) to {label} list.')
    return games

### Collection Logic ###

def manage_collection():
    while True:
        games = read_file(COLLECTION_FILE)
        print("\n[Game Collection]")
        list_games(games)
        print("\nCommands: add | remove | refresh | quit")
        cmd = input("Command: ").strip().lower()
        if cmd in ('quit', 'q', 'exit'):
            break
        elif cmd in ('add', 'a'):
            games = add_game(games)
            write_file(COLLECTION_FILE, games)
        elif cmd in ('remove', 'r'):
            games = remove_game(games)
            write_file(COLLECTION_FILE, games)
        elif cmd in ('refresh', ''):
            continue
        else:
            print("Invalid command.")

### Wishlist Logic ###

def manage_wishlist():
    while True:
        wishlist = read_file(WISHLIST_FILE)
        print("\n[Wishlist]")
        list_games(wishlist, label="wishlist item")
        print("\nCommands: add | remove | refresh | quit")
        cmd = input("Command: ").strip().lower()
        if cmd in ('quit', 'q', 'exit'):
            break
        elif cmd in ('add', 'a'):
            wishlist = add_game(wishlist, label="wishlist item")
            write_file(WISHLIST_FILE, wishlist)
        elif cmd in ('remove', 'r'):
            wishlist = remove_game(wishlist, label="wishlist item")
            write_file(WISHLIST_FILE, wishlist)
        elif cmd in ('refresh', ''):
            continue
        else:
            print("Invalid command.")

### Main Menu ###

def main_menu():
    print(f"\n{'='*40}\n{PROGRAM_NAME} {VERSION}\n{TAGLINE}\n{'='*40}")
    while True:
        print("\nMain Menu - enter a command or number:")
        print("  1. view     - View/manage collection")
        print("  2. add      - Add a new game to collection")
        print("  3. about    - About this program")
        print("  4. help     - How to use")
        print("  5. quit     - Exit program")
        print("  6. wishlist - View/manage wishlist")
        choice = input("Command: ").strip().lower()
        if choice in ('1', 'view', 'manage'):
            manage_collection()
        elif choice in ('2', 'add', 'a'):
            games = read_file(COLLECTION_FILE)
            games = add_game(games)
            write_file(COLLECTION_FILE, games)
        elif choice in ('3', 'about'):
            print(ABOUT_TEXT)
        elif choice in ('4', 'help'):
            print(HELP_TEXT)
        elif choice in ('5', 'quit', 'exit'):
            print("Goodbye!")
            break
        elif choice in ('6', 'wishlist', 'w'):
            manage_wishlist()
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main_menu()
