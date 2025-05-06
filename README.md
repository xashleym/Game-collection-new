# Game Collection Manager

A simple terminal microservice for managing a game collection and wishlist using plain text files as communication pipes.

## How it Works

- **game_collection.txt**: Stores your game collection (`Title|Genre` per line).
- **wishlist.txt**: Stores your wishlist (`Title|Genre` per line).
- Both files act as "communication pipes" — multiple scripts or terminals can read/write them at once, simulating microservice IPC.

## Features

- Add, view, and remove games from your collection.
- (Extendable) Manage your wishlist in the same way.
- About and Help menus for guidance.

## Usage

python manage_collection.py

Follow the menu prompts to add, view, or remove games. Files are created automatically.
