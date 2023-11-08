import keyboard

KEY_DOWN = True
KEY_UP = False

KEYS = {
    "left arrow" : KEY_UP,
    "right arrow" : KEY_UP,
    "up arrow" : KEY_UP,
    "down arrow" : KEY_UP,
    "enter" : KEY_UP,
    "esc" : KEY_UP
}

def getKeys():
    return KEYS

def update():
    global KEY
    for key in KEYS.keys():
        KEYS[key] = KEY_DOWN if keyboard.is_pressed(key) else KEY_UP