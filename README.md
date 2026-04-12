# Paranoia
Paranoia is a 4 person horror LAN multiplayer game.
You are at a haunted house with a gun and a flashlight. Three other people are in the house. Will you survive?

# Installation

## Requirements
- Python 3.6 or higher
- pip

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Paranoia
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:
- **Windows:**
```bash
.venv\Scripts\activate
```
- **macOS/Linux:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install PyOpenGL PyOpenGL_accelerate numpy
```

## Running the Game

1. Start the server:
```bash
python server.py
```

2. Run the game client (on each player's machine):
```bash
python Paranoia.py
```

# Features
  1. 4-person LAN multiplayer.
  2. Limited sight for players to simulate dark house.
  3. Unique map.
  4. Minimap.
  5. Limited time power-ups to gain advantage.
# Devs
This game was made for our CSE423 project.
