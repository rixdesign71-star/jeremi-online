"""
JEREMI Online Multiplayer Server
Run: python server.py
Then open http://localhost:5000 in any browser on any device on the same WiFi.
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
import random
import unicodedata
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jeremi-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# ─────────────────────────────────────────────────────────────
# TILE DATA  (exactly from your Python file)
# ─────────────────────────────────────────────────────────────
ALL_TILES = {
    "m":  {"count":2,  "points":4,  "type":"base_consonant"},
    "ɱ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "n":  {"count":2,  "points":4,  "type":"base_consonant"},
    "ɲ":  {"count":6,  "points":2,  "type":"base_consonant"},
    "ŋ":  {"count":4,  "points":3,  "type":"base_consonant"},
    "ɴ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ŋm": {"count":8,  "points":1,  "type":"base_consonant"},
    "p":  {"count":2,  "points":4,  "type":"base_consonant"},
    "b":  {"count":2,  "points":4,  "type":"base_consonant"},
    "t":  {"count":2,  "points":4,  "type":"base_consonant"},
    "d":  {"count":2,  "points":4,  "type":"base_consonant"},
    "c":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ɟ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "k":  {"count":2,  "points":4,  "type":"base_consonant"},
    "g":  {"count":2,  "points":4,  "type":"base_consonant"},
    "q":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ɢ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ʔ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "kp": {"count":2,  "points":4,  "type":"base_consonant"},
    "gb": {"count":4,  "points":3,  "type":"base_consonant"},
    "pʼ": {"count":8,  "points":1,  "type":"base_consonant"},
    "tʼ": {"count":8,  "points":1,  "type":"base_consonant"},
    "cʼ": {"count":8,  "points":1,  "type":"base_consonant"},
    "kʼ": {"count":8,  "points":1,  "type":"base_consonant"},
    "qʼ": {"count":8,  "points":1,  "type":"base_consonant"},
    "ʘ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "[":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ǃ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ǂ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "pɸ": {"count":8,  "points":1,  "type":"base_consonant"},
    "bβ": {"count":8,  "points":1,  "type":"base_consonant"},
    "ts": {"count":8,  "points":1,  "type":"base_consonant"},
    "dz": {"count":8,  "points":1,  "type":"base_consonant"},
    "tʃ": {"count":8,  "points":1,  "type":"base_consonant"},
    "dʒ": {"count":8,  "points":1,  "type":"base_consonant"},
    "kx": {"count":8,  "points":1,  "type":"base_consonant"},
    "gɣ": {"count":8,  "points":1,  "type":"base_consonant"},
    "ɸ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "β":  {"count":8,  "points":1,  "type":"base_consonant"},
    "f":  {"count":4,  "points":3,  "type":"base_consonant"},
    "v":  {"count":6,  "points":2,  "type":"base_consonant"},
    "s":  {"count":2,  "points":4,  "type":"base_consonant"},
    "z":  {"count":6,  "points":2,  "type":"base_consonant"},
    "ʃ":  {"count":6,  "points":2,  "type":"base_consonant"},
    "ʒ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ç":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ʝ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "x":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ɣ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "χ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ʁ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ħ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ʕ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "h":  {"count":8,  "points":1,  "type":"base_consonant"},
    "ʋ":  {"count":8,  "points":1,  "type":"base_consonant"},
    "r":  {"count":4,  "points":3,  "type":"base_consonant"},
    "j":  {"count":2,  "points":4,  "type":"base_consonant"},
    "w":  {"count":2,  "points":4,  "type":"base_consonant"},
    "l":  {"count":2,  "points":4,  "type":"base_consonant"},
    "i":  {"count":1,  "points":20, "type":"base_vowel"},
    "e":  {"count":3,  "points":13, "type":"base_vowel"},
    "ɛ":  {"count":5,  "points":8,  "type":"base_vowel"},
    "a":  {"count":1,  "points":20, "type":"base_vowel"},
    "ɔ":  {"count":1,  "points":16, "type":"base_vowel"},
    "o":  {"count":3,  "points":11, "type":"base_vowel"},
    "u":  {"count":3,  "points":14, "type":"base_vowel"},
    "ɪ":  {"count":8,  "points":2,  "type":"base_vowel"},
    "ʊ":  {"count":8,  "points":3,  "type":"base_vowel"},
    "ʷ":  {"count":12, "points":2,  "type":"diacritic"},
    "ʲ":  {"count":12, "points":1,  "type":"diacritic"},
    "̩":   {"count":12, "points":2,  "type":"diacritic"},
    "ˤ":  {"count":12, "points":1,  "type":"diacritic"},
    "ː":  {"count":8,  "points":7,  "type":"diacritic"},
    "̃":   {"count":4,  "points":14, "type":"diacritic"},
    "ˬ":  {"count":8,  "points":3,  "type":"diacritic"},
}

BONUS_SQUARES = {
    (0,9):"TM",(2,7):"TM",(7,7):"TM",(12,8):"TM",(14,5):"TM",
    (12,0):"DS",(2,14):"DS",(13,1):"TL",(1,13):"TL",
    (12,2):"DS",(2,12):"DS",(11,3):"DL",(3,11):"DL",
    (10,4):"DS",(4,10):"DS",(8,4):"DM",(6,10):"DM",
    (9,5):"DL",(5,9):"DL",(10,6):"DS",(4,8):"DS",
    (10,8):"DS",(4,6):"DS",(9,9):"DM",(5,5):"DM",
    (8,10):"DM",(6,4):"DM",(10,10):"DS",(4,4):"DS",
    (11,11):"DL",(3,3):"DL",(12,12):"DM",(2,2):"DM",
    (13,13):"TL",(1,1):"TL",(14,12):"DM",(0,2):"DM",
}
SR, SC = 7, 0

VOWELS       = {"i","e","ɛ","a","ɔ","o","u","ɪ","ʊ"}
GLIDES       = {"j","w"}
NASALS       = {"m","n","ɲ","ŋ","ɴ","ŋm"}
ROUNDED_V    = {"u","o","ɔ"}
FRONT_HIGH_V = {"i","e"}
PHARYNGEALS  = {"ħ","ʕ"}

_RAW_DIAC = [
    "mʷ","ŋʷ","kʷ","gʷ","dʲ","gʲ",
    "m̩","ɱ̩","n̩","ɲ̩","ŋ̩","ŋm̩","lˤ",
    "iː","eː","ɛː","aː","ɔː","oː","uː",
    "ĩ","ẽ","ɛ̃","ã","ɔ̃","õ","ũ",
    "pˬ","tˬ","kˬ","fˬ","sˬ","ʃˬ","θˬ","xˬ","χˬ","ħˬ","hˬ",
    "tsˬ","tʃˬ","kxˬ","pɸˬ","cˬ","qˬ",
]
DIAC_COMBOS = {unicodedata.normalize("NFC", c) for c in _RAW_DIAC}

SYL_NASALS = {"m̩","ɱ̩","n̩","ɲ̩","ŋ̩","ŋm̩"}

def build_ext_vowels():
    ev = set(VOWELS)
    for v in ["iː","eː","ɛː","aː","ɔː","oː","uː","ĩ","ẽ","ɛ̃","ã","ɔ̃","õ","ũ"]:
        ev.add(unicodedata.normalize("NFC", v))
    return ev
EXT_VOWELS = build_ext_vowels()

# ─────────────────────────────────────────────────────────────
# GAME STATE  (one state dict per room)
# ─────────────────────────────────────────────────────────────
rooms = {}   # room_code -> game state
# socket_id -> {room, player_index}
connections = {}

def new_game_state(player_names):
    bag = []
    for sym, info in ALL_TILES.items():
        for _ in range(info["count"]):
            bag.append({"symbol": sym, "points": info["points"], "type": info["type"]})
    for _ in range(6):
        bag.append({"symbol": None, "points": 0, "type": "blank"})
    random.shuffle(bag)

    board = [[None]*15 for _ in range(15)]
    for (r,c), bonus in BONUS_SQUARES.items():
        board[r][c] = {"bonus": bonus}
    board[SR][SC] = {"start": True}

    players = [{"name": n, "hand": [], "score": 0, "skip": False} for n in player_names]

    # Draw unique tiles to determine first player
    used = set()
    draws = []
    for p in players:
        available = [i for i in range(len(bag)) if i not in used]
        idx = random.choice(available)
        used.add(idx)
        draws.append({"player_idx": players.index(p), "tile": bag[idx]})
    draws.sort(key=lambda d: d["tile"]["points"], reverse=True)
    first_idx = draws[0]["player_idx"]

    # Deal 9 tiles to each player
    for p in players:
        for _ in range(9):
            if bag:
                ri = random.randint(0, len(bag)-1)
                p["hand"].append(bag.pop(ri))

    return {
        "board": board,
        "bag": bag,
        "players": players,
        "current_idx": first_idx,
        "turn_number": 1,
        "history": [],
        "consecutive_passes": 0,
        "board_has_tiles": False,
        "phase": "playing",   # playing | ended
        "draws": draws,       # for the draw modal
    }

def draw_tiles(state, n):
    drawn = []
    for _ in range(n):
        if not state["bag"]: break
        idx = random.randint(0, len(state["bag"])-1)
        drawn.append(state["bag"].pop(idx))
    return drawn

def replenish(state, player_idx):
    p = state["players"][player_idx]
    needed = 9 - len(p["hand"])
    if needed > 0:
        p["hand"].extend(draw_tiles(state, needed))

# ─────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────
def is_vowel_like(s):
    return s in EXT_VOWELS or s in SYL_NASALS

def is_cons(s):
    return not is_vowel_like(s)

def split_syllables(syms):
    sl = []
    i = 0
    while i < len(syms):
        s = syms[i]
        if s in SYL_NASALS:
            sl.append([s]); i += 1; continue
        if i+2 < len(syms) and is_cons(s) and syms[i+1] in GLIDES and is_vowel_like(syms[i+2]):
            sl.append(syms[i:i+3]); i += 3; continue
        if i+1 < len(syms) and is_cons(s) and is_vowel_like(syms[i+1]):
            sl.append(syms[i:i+2]); i += 2; continue
        if is_vowel_like(s):
            sl.append([s]); i += 1; continue
        return None
    return sl

def validate_word(tiles):
    syms = [t["tile"]["symbol"] for t in tiles if t["tile"].get("type") != "boundary"]
    if not syms:
        return False, "No tiles"
    sl = split_syllables(syms)
    if sl is None:
        return False, f"Invalid syllable structure: /{' '.join(syms)}/. Only CV, V, CGV."
    root = list(syms)
    if root and root[0] == "i" and len(root) > 1:
        root = root[1:]
    if len(root) >= 2 and root[-2] == "n" and root[-1] == "ɛ":
        root = root[:-2]
    rs = split_syllables(root)
    if rs and len(rs) > 3:
        return False, f"Root exceeds 3 syllables ({len(rs)} found)"
    if syms[0] == "i" and len(syms) > 1 and syms[1] in VOWELS:
        return False, "Negation [i] only on verbs"
    for i in range(len(syms)-1):
        s1, s2 = syms[i], syms[i+1]
        if is_cons(s1) and s1 not in SYL_NASALS and is_cons(s2) and s2 not in SYL_NASALS:
            if s2 in GLIDES and i+2 < len(syms) and is_vowel_like(syms[i+2]):
                continue
            if s1 in GLIDES and not is_vowel_like(s2):
                return False, f"Glide /{s1}/ must precede vowel"
            if s2 not in GLIDES:
                return False, f"Illegal cluster: /{s1}{s2}/"
    return True, None

# ─────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────
def identify_morphemes(tiles):
    syms = [t["tile"]["symbol"] for t in tiles]
    morphs = []
    start, end = 0, len(tiles)
    if syms and syms[0] == "i":
        morphs.append({"type":"prefix","tiles":[tiles[0]]}); start = 1
    has_suf = len(syms) >= 2 and syms[-2] == "n" and syms[-1] == "ɛ"
    if has_suf: end = len(tiles)-2
    morphs.append({"type":"root","tiles":tiles[start:end]})
    if has_suf: morphs.append({"type":"suffix","tiles":tiles[-2:]})
    return morphs

def score_word(tiles, placed_positions):
    wm = 1
    for t in tiles:
        k = (t["row"], t["col"])
        if k not in placed_positions: continue
        b = BONUS_SQUARES.get(k)
        if b == "TL" and wm < 3: wm = 3
        elif b == "DL" and wm < 2: wm = 2

    for t in tiles:
        k = (t["row"], t["col"])
        b = BONUS_SQUARES.get(k)
        t["sc"] = t["tile"]["points"]
        if k in placed_positions and b == "DS":
            t["sc"] *= 2

    not_bnd = [t for t in tiles if t["tile"].get("type") != "boundary"]
    morphs = identify_morphemes(not_bnd)
    total = 0
    for m in morphs:
        ms = sum(t["sc"] for t in m["tiles"])
        mm = 1
        for t in m["tiles"]:
            k = (t["row"], t["col"])
            if k not in placed_positions: continue
            b = BONUS_SQUARES.get(k)
            if b == "TM" and mm < 3: mm = 3
            elif b == "DM" and mm < 2: mm = 2
        total += ms * mm
    return total * wm

# ─────────────────────────────────────────────────────────────
# WORD READING
# ─────────────────────────────────────────────────────────────
def get_connected(board, sr, sc, direction):
    tiles = []
    if direction == "h":
        c = sc
        while c > 0 and board[sr][c-1] and board[sr][c-1].get("tile") and board[sr][c-1]["tile"].get("type") != "boundary":
            c -= 1
        while c < 15 and board[sr][c] and board[sr][c].get("tile") and board[sr][c]["tile"].get("type") != "boundary":
            tiles.append({"tile": board[sr][c]["tile"], "row": sr, "col": c})
            c += 1
    else:
        r = sr
        while r > 0 and board[r-1][sc] and board[r-1][sc].get("tile") and board[r-1][sc]["tile"].get("type") != "boundary":
            r -= 1
        while r < 15 and board[r][sc] and board[r][sc].get("tile") and board[r][sc]["tile"].get("type") != "boundary":
            tiles.append({"tile": board[r][sc]["tile"], "row": r, "col": sc})
            r += 1
    return tiles

def get_all_words(board, real_placed):
    if not real_placed: return []
    rows = [p["row"] for p in real_placed]
    cols = [p["col"] for p in real_placed]
    if len(real_placed) == 1:
        md, cd = "h", "v"
    elif len(set(rows)) == 1:
        md, cd = "h", "v"
    else:
        md, cd = "v", "h"

    words = []
    if md == "h":
        mw = get_connected(board, rows[0], min(cols), "h")
    else:
        mw = get_connected(board, min(rows), cols[0], "v")
    if len(mw) > 1: words.append(mw)
    elif len(real_placed) == 1:
        v = get_connected(board, real_placed[0]["row"], real_placed[0]["col"], "v")
        h = get_connected(board, real_placed[0]["row"], real_placed[0]["col"], "h")
        if len(v) > 1: words.append(v)
        if len(h) > 1: words.append(h)
        return words

    seen = set()
    for p in real_placed:
        cw = get_connected(board, p["row"], p["col"], cd)
        key = (cw[0]["row"], cw[0]["col"], cw[-1]["row"], cw[-1]["col"]) if cw else None
        if key and len(cw) > 1 and key not in seen:
            seen.add(key); words.append(cw)
    return words

# ─────────────────────────────────────────────────────────────
# PUBLIC STATE  (what every client receives — hides other players' hands)
# ─────────────────────────────────────────────────────────────
def public_state(state, for_player_idx):
    players_pub = []
    for i, p in enumerate(state["players"]):
        pub = {
            "name":  p["name"],
            "score": p["score"],
            "tiles": len(p["hand"]),
            "skip":  p["skip"],
        }
        if i == for_player_idx:
            pub["hand"] = p["hand"]
        players_pub.append(pub)

    return {
        "board":        state["board"],
        "bag_count":    len(state["bag"]),
        "players":      players_pub,
        "current_idx":  state["current_idx"],
        "turn_number":  state["turn_number"],
        "history":      state["history"],
        "phase":        state["phase"],
        "my_idx":       for_player_idx,
    }

def broadcast_state(room_code):
    state = rooms[room_code]
    for sid, info in list(connections.items()):
        if info["room"] == room_code:
            pi = info["player_idx"]
            socketio.emit("state_update", public_state(state, pi), to=sid)

# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─────────────────────────────────────────────────────────────
# SOCKET EVENTS
# ─────────────────────────────────────────────────────────────
@socketio.on("connect")
def on_connect():
    print(f"Client connected: {request.sid}")

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    if sid in connections:
        info = connections.pop(sid)
        room = info["room"]
        print(f"Player {info['player_idx']} disconnected from room {room}")

@socketio.on("create_room")
def on_create_room(data):
    """Host creates a room and starts the game."""
    names = data.get("names", [])
    if len(names) < 2 or len(names) > 4:
        emit("error", {"msg": "Need 2-4 player names"})
        return

    # Generate a short room code
    code = str(random.randint(1000, 9999))
    while code in rooms:
        code = str(random.randint(1000, 9999))

    state = new_game_state(names)
    rooms[code] = state

    # Host is player 0 (first in the list)
    connections[request.sid] = {"room": code, "player_idx": 0}
    join_room(code)

    emit("room_created", {
        "code": code,
        "draw_results": state["draws"],
        "first_player": state["players"][state["current_idx"]]["name"],
        "my_idx": 0,
    })

    # Send initial state to host
    emit("state_update", public_state(state, 0))

@socketio.on("join_room")
def on_join_room(data):
    """A remote player joins a room by code."""
    code = data.get("code", "").strip()
    name = data.get("name", "").strip()

    if code not in rooms:
        emit("error", {"msg": f"Room {code} not found"})
        return

    state = rooms[code]
    if state["phase"] != "playing":
        emit("error", {"msg": "Game already ended"})
        return

    # Find which player slot this person is
    # They must have been added by the host with their name
    player_idx = None
    for i, p in enumerate(state["players"]):
        if p["name"] == name:
            # Check not already connected
            already = any(
                c["room"] == code and c["player_idx"] == i
                for c in connections.values()
            )
            if not already:
                player_idx = i
                break

    if player_idx is None:
        emit("error", {"msg": f"Name '{name}' not found in this room, or already connected"})
        return

    connections[request.sid] = {"room": code, "player_idx": player_idx}
    join_room(code)

    emit("joined_room", {
        "code": code,
        "my_idx": player_idx,
        "draw_results": state["draws"],
        "first_player": state["players"][state["current_idx"]]["name"],
    })
    emit("state_update", public_state(state, player_idx))

@socketio.on("play_tiles")
def on_play_tiles(data):
    """
    Player submits their placed tiles.
    data = {placements: [{row, col, tile, isDiac, prevSym, prevPts}, ...]}
    Server validates, scores, stores.
    """
    sid = request.sid
    if sid not in connections:
        emit("error", {"msg": "Not in a room"}); return
    info = connections[sid]
    room, pi = info["room"], info["player_idx"]
    state = rooms[room]

    if state["current_idx"] != pi:
        emit("error", {"msg": "Not your turn"}); return

    placements = data.get("placements", [])
    real_placed = [p for p in placements if not p.get("isDiac") and not p.get("isBnd")]
    board = state["board"]

    if not real_placed:
        emit("play_error", {"msg": "Place at least one tile"}); return

    # Apply placements to board temporarily
    rollback = []
    for pl in placements:
        r, c = pl["row"], pl["col"]
        prev = board[r][c]
        rollback.append((r, c, prev))
        if pl.get("isDiac"):
            if board[r][c] and board[r][c].get("tile"):
                board[r][c]["tile"]["symbol"] = pl["newSym"]
                board[r][c]["tile"]["points"] = pl["newPts"]
                board[r][c]["tile"]["diacritic"] = pl["diac"]
        elif pl.get("isBnd"):
            board[r][c] = {"tile": {"symbol":"#","points":0,"type":"boundary"}, "bonus": None}
        else:
            board[r][c] = {"tile": pl["tile"], "bonus": BONUS_SQUARES.get((r,c))}

    def rollback_board():
        for r, c, prev in rollback:
            board[r][c] = prev

    # First move check
    if not state["board_has_tiles"]:
        if not any(p["row"] == SR and p["col"] == SC for p in real_placed):
            rollback_board()
            emit("play_error", {"msg": "First word must cover the START square (R8 C1)"}); return

    # Connection check
    if state["board_has_tiles"]:
        placed_set = {(p["row"],p["col"]) for p in real_placed}
        connected = False
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        for p in real_placed:
            for dr,dc in dirs:
                nr,nc = p["row"]+dr, p["col"]+dc
                if 0<=nr<15 and 0<=nc<15 and (nr,nc) not in placed_set:
                    cell = board[nr][nc]
                    if cell and cell.get("tile"):
                        connected = True; break
            if connected: break
        if not connected:
            rollback_board()
            emit("play_error", {"msg": "Word must connect to existing tiles"}); return

    # Gap check
    rows = [p["row"] for p in real_placed]
    cols = [p["col"] for p in real_placed]
    if len(real_placed) > 1:
        if len(set(rows)) == 1:
            for c in range(min(cols), max(cols)+1):
                cl = board[rows[0]][c]
                if not cl or (not cl.get("tile") and not cl.get("bonus") and not cl.get("start")):
                    rollback_board()
                    emit("play_error", {"msg": "Gap between tiles!"}); return
        else:
            for r in range(min(rows), max(rows)+1):
                cl = board[r][cols[0]]
                if not cl or (not cl.get("tile") and not cl.get("bonus") and not cl.get("start")):
                    rollback_board()
                    emit("play_error", {"msg": "Gap between tiles!"}); return

    # Word validation
    words = get_all_words(board, real_placed)
    if not words:
        rollback_board()
        emit("play_error", {"msg": "No word formed"}); return

    for wt in words:
        valid, reason = validate_word(wt)
        if not valid:
            rollback_board()
            emit("play_error", {"msg": reason}); return

    # Scoring
    placed_positions = {(p["row"],p["col"]) for p in real_placed}
    total = sum(score_word(wt, placed_positions) for wt in words)
    if len(real_placed) == 9: total += 30

    word_str = "".join(t["tile"]["symbol"] for t in words[0] if t["tile"]["symbol"] != "#")

    # Remove tiles from player's hand
    player = state["players"][pi]
    tile_syms_to_remove = [pl["tile"]["symbol"] for pl in real_placed if not pl.get("isDiac") and not pl.get("isBnd")]
    for sym in tile_syms_to_remove:
        for j, ht in enumerate(player["hand"]):
            if ht["symbol"] == sym:
                player["hand"].pop(j); break

    # Store pending score for challenge window
    state["pending"] = {
        "score": total,
        "word_str": word_str,
        "player_idx": pi,
        "placements": placements,
        "rollback": rollback,
    }

    # Notify all players — show challenge modal to the NEXT player
    ni = (pi+1) % len(state["players"])
    socketio.emit("challenge_prompt", {
        "word": word_str,
        "score": total,
        "played_by": player["name"],
        "challenger_idx": ni,
    }, to=room)

@socketio.on("challenge_response")
def on_challenge_response(data):
    """Next player decides to challenge or accept."""
    sid = request.sid
    if sid not in connections: return
    info = connections[sid]
    room, pi = info["room"], info["player_idx"]
    state = rooms[room]
    pending = state.get("pending")
    if not pending: return

    accept = data.get("accept", True)
    played_idx = pending["player_idx"]
    player = state["players"][played_idx]

    if accept:
        # Add score, replenish hand
        player["score"] += pending["score"]
        state["board_has_tiles"] = True
        state["history"].append({
            "tn": state["turn_number"],
            "player": player["name"],
            "word": pending["word_str"],
            "score": pending["score"],
        })
        replenish(state, played_idx)
        state["consecutive_passes"] = 0
        state.pop("pending", None)
        socketio.emit("play_accepted", {
            "player": player["name"],
            "word": pending["word_str"],
            "score": pending["score"],
        }, to=room)
    else:
        # Challenge upheld — rollback board, deduct score
        board = state["board"]
        for r, c, prev in pending["rollback"]:
            board[r][c] = prev
        # Return tiles to player's hand
        for pl in pending["placements"]:
            if not pl.get("isDiac") and not pl.get("isBnd"):
                player["hand"].append(pl["tile"])
        player["score"] = max(0, player["score"] - pending["score"])
        # Challenger loses next turn
        state["players"][pi]["skip"] = True
        state.pop("pending", None)
        socketio.emit("play_challenged", {
            "player": player["name"],
            "challenger": state["players"][pi]["name"],
        }, to=room)

    # Advance turn
    _advance_turn(state, room)
    broadcast_state(room)

@socketio.on("pass_turn")
def on_pass(data):
    sid = request.sid
    if sid not in connections: return
    info = connections[sid]
    room, pi = info["room"], info["player_idx"]
    state = rooms[room]
    if state["current_idx"] != pi: return

    state["consecutive_passes"] += 1
    state["history"].append({
        "tn": state["turn_number"],
        "player": state["players"][pi]["name"],
        "word": "pass", "score": "",
    })
    _advance_turn(state, room)
    broadcast_state(room)

@socketio.on("replace_tiles")
def on_replace(data):
    sid = request.sid
    if sid not in connections: return
    info = connections[sid]
    room, pi = info["room"], info["player_idx"]
    state = rooms[room]
    if state["current_idx"] != pi: return

    indices = sorted(data.get("indices", []), reverse=True)
    player = state["players"][pi]
    removed = [player["hand"].pop(i) for i in indices if i < len(player["hand"])]
    player["hand"].extend(draw_tiles(state, len(removed)))
    state["bag"].extend(removed)
    random.shuffle(state["bag"])
    state["history"].append({
        "tn": state["turn_number"],
        "player": player["name"],
        "word": "replaced", "score": "",
    })
    state["consecutive_passes"] = 0
    _advance_turn(state, room)
    broadcast_state(room)

def _advance_turn(state, room):
    state["turn_number"] += 1
    n = len(state["players"])
    next_idx = (state["current_idx"]+1) % n
    # Skip penalised players
    attempts = 0
    while state["players"][next_idx]["skip"] and attempts < n:
        state["players"][next_idx]["skip"] = False
        next_idx = (next_idx+1) % n
        attempts += 1
    state["current_idx"] = next_idx

    # Check game over
    if state["consecutive_passes"] >= n*2:
        _end_game(state); return
    if not state["bag"] and any(len(p["hand"])==0 for p in state["players"]):
        _end_game(state)

def _end_game(state):
    state["phase"] = "ended"
    fin = next((p for p in state["players"] if len(p["hand"])==0), None)
    leftover = 0
    for p in state["players"]:
        if p["hand"]:
            lv = sum(t["points"] for t in p["hand"])
            p["score"] -= lv
            leftover += lv
    if fin: fin["score"] += leftover

if __name__ == "__main__":
    print("=" * 50)
    print("  JEREMI Online Server")
    print("  Open http://localhost:5000 in your browser")
    print("  Other devices on same WiFi: http://<your-ip>:5000")
    print("=" * 50)
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
