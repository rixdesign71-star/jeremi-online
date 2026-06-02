JEREMI Online Multiplayer
========================

SETUP (one time only)
---------------------
1. Make sure Python is installed (python.org)
2. Open a terminal / command prompt in this folder
3. Run:  pip install -r requirements.txt

START THE SERVER
----------------
Run:  python server.py

You will see:
  JEREMI Online Server
  Open http://localhost:5000 in your browser
  Other devices on same WiFi: http://<your-ip>:5000

TO FIND YOUR IP ADDRESS
------------------------
Windows:  open Command Prompt → type  ipconfig  → look for "IPv4 Address"
Mac/Linux: open Terminal → type  ifconfig  → look for "inet"

Example: if your IP is 192.168.1.5, other players go to http://192.168.1.5:5000

HOW TO PLAY
-----------
HOST (you):
  1. Open http://localhost:5000
  2. Click "Host Game"
  3. Enter all player names (2-4)
  4. Click "Create Room"
  5. Share the 4-digit room code with other players

OTHER PLAYERS:
  1. Open http://<host-ip>:5000 on their device
  2. Click "Join Game"
  3. Enter the room code and their name (must match what host entered)
  4. Click "Join Room"

GAMEPLAY:
  - Drag tiles from your rack onto the board
  - Diacritic tiles glow orange on valid base tiles
  - Click "Done" when your word is ready
  - Next player sees a challenge window — accept or challenge
  - Only YOUR rack is visible to you

FILES
-----
server.py         — the game server (run this)
requirements.txt  — Python packages needed
templates/
  index.html      — the game frontend (served automatically)
