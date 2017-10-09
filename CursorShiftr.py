__author__ = 'Charlie'
import ctypes
import win32api
import time
import random

SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event
mouse_pos = win32api.GetCursorPos

# following two (dx and dy) args mean the new screen position of the mouse
absolmove = 0x8000
# following two (dx and dy) args mean the change in screen position of the mouse
relmove = 0x0001
# presses left mouse button
leftdown = 0x0002
# releases it
leftup = 0x0004
# presses middle mouse button
middown = 0x0020
# releases it
midup = 0x0040
# presses right mouse button
rightdown = 0x0008
# releases it
rightup = 0x0010
# mouse wheel rolled up by units in fourth arg (dwData)
wheelmove = 0x0800
# mouse wheel tilted right by amount in fourth arg (dwData)
wheeltilt = 0x01000


def mousemove(x, y):
    mouse_event(relmove, x, y, 0, 0)


def mouseset(x, y):
    mouse_event(absolmove, x, y, 0, 0)

while True:
    mode = input("set mode ")
    if mode == "wind":
        print("Watch out, there's an ill wind blowing...")
        i = 1
        # xy cursor wind direction
        direction = [1, 0]
        while True:
            # moves mouse according to set wind directions
            mousemove(direction[0], direction[1])
            # random xy directions set
            if i == 0:
                for j in range(0, 2):
                    rand = random.randrange(0, 3)
                    if rand < 1:
                        direction[j] = -1
                    elif rand < 2:
                        direction[j] = 0
                    else:
                        direction[j] = 1
            time.sleep(0.02)
            i = (i + 1) % 200
    elif mode == "mouse":
        print("Your mouse is now awesome!")
        i = 0
        # makes 50% duty cycle, 1Hz beeps with frequency according to mouseX position
        while True:
            xpos, ypos = mouse_pos()
            win32api.Beep(xpos, 500)
            time.sleep(0.5)
    elif mode == "keys":
        print("Your keyboard is now awesome!")

        def noises(topkey, lowkey, topfreq=20000, lowfreq=20, *exclude):
            # makes bleeps by mapping the keyboard Vkeys onto frequencies between two bounds
            # excludes any leftover keys you don't want to include
            # checks which keys pressed from range
            nolist = []
            for m in range(lowkey, topkey + 1):
                if exclude.count(m) == 0:
                    if win32api.GetAsyncKeyState(m) < 0:
                        nolist.append(m)
            # and beeps accordingly for sci-fi keyboard effect!
            k = 0
            while k < len(nolist):
                # map keys onto frequencies
                fraction = (nolist[k] - (lowkey - 1)) / (topkey - (lowkey - 1))
                freq = int(fraction * (topfreq - (lowfreq - 1)))
                # makes beeps
                win32api.Beep(freq, 100)
                k += 1
        while True:
            # check keys and make noises
            noises(0x5A, 0x41, 5000, 1000)  # for letters
            noises(0x39, 0x30, 800, 200)  # for numbers
            noises(0x24, 0x20, 1200, 800)  # assorted arrow keys and so on and spacebar
            noises(0x69, 0x60, 800, 200)  # numpad numbers
            noises(0x7B, 0x70, 5000, 3800)  # function buttons 1-12
    elif mode == "keys2":
        octaves = [[16.35,  17.32,  18.35,  19.45,  20.6,   21.83,  23.12,  24.5, 25.96,  27.5, 29.14,  30.87],
                   [24.65,  32.7,   36.71,  38.89,  41.2,   43.65,  46.25,  49,   51.91,  55,   58.27,  61.74],
                   [65.41,  69.3,   73.42,  77.78,  82.41,  87.31,  92.5,   98,   103.83, 110,  116.54, 123.47],
                   [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185,    196,  207.65, 220,  233.08, 246.94],
                   [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392,  415,    440,  466.16, 493.88]]

        def sounds(topkey, lowkey, *exclude):
            nolist = []
            for m in range(lowkey, topkey + 1):
                if exclude.count(m) == 0:
                    if win32api.GetAsyncKeyState(m) < 0:
                        nolist.append(m)
            # and beeps accordingly for sci-fi keyboard effect!
            k = 0
            while k < len(nolist):
                # map keys onto frequencies
                note = nolist[k] - lowkey
                octave = 2
                while note >= 12:
                    note -= 12
                    octave += 1
                freq = int(octaves[octave][note])
                # makes beeps
                win32api.Beep(freq, 100)
                k += 1
            return True
        while True:
            sounds(0x5A, 0x41)
            sounds(0x39, 0x30)
            sounds(0x24, 0x20)
            sounds(0x69, 0x60)
            sounds(0x7B, 0x70)
    elif mode == "keys3":
        def sounds(topkey, lowkey, *exclude):
            nolist = []
            for m in range(lowkey, topkey + 1):
                if exclude.count(m) == 0:
                    if win32api.GetAsyncKeyState(m) < 0:
                        nolist.append(m)
            # and beeps accordingly for sci-fi keyboard effect!
            k = 0
            while k < len(nolist):
                # map keys onto frequencies
                n = (nolist[k] - lowkey) + 24
                freq = int(pow(2,(n-49) / 12) * 440)
                # makes beeps
                win32api.Beep(freq, 100)
                k += 1
            return True
        while True:
            sounds(0x5A, 0x41)
            sounds(0x39, 0x30)
            sounds(0x24, 0x20)
            sounds(0x69, 0x60)
            sounds(0x7B, 0x70)
    else:
        print("Sorry, don't have one called %s" % mode)

# and here, the buttons for reference,
# each number being preceded by the VK_ notation and followed by function
"""
VK_LBUTTON
0x01
Left mouse button
VK_RBUTTON
0x02
Right mouse button
VK_CANCEL
0x03
Control-break processing
VK_MBUTTON
0x04
Middle mouse button (three-button mouse)
VK_XBUTTON1
0x05
X1 mouse button
VK_XBUTTON2
0x06
X2 mouse button
-
0x07
Undefined
VK_BACK
0x08
BACKSPACE key
VK_TAB
0x09
TAB key
-
0x0A-0B
Reserved
VK_CLEAR
0x0C
CLEAR key
VK_RETURN
0x0D
ENTER key
-
0x0E-0F
Undefined
VK_SHIFT
0x10
SHIFT key
VK_CONTROL
0x11
CTRL key
VK_MENU
0x12
ALT key
VK_PAUSE
0x13
PAUSE key
VK_CAPITAL
0x14
CAPS LOCK key
VK_KANA
0x15
IME Kana mode
VK_HANGUEL
0x15
IME Hanguel mode (maintained for compatibility; use VK_HANGUL)
VK_HANGUL
0x15
IME Hangul mode
-
0x16
Undefined
VK_JUNJA
0x17
IME Junja mode
VK_FINAL
0x18
IME final mode
VK_HANJA
0x19
IME Hanja mode
VK_KANJI
0x19
IME Kanji mode
-
0x1A
Undefined
VK_ESCAPE
0x1B
ESC key
VK_CONVERT
0x1C
IME convert
VK_NONCONVERT
0x1D
IME nonconvert
VK_ACCEPT
0x1E
IME accept
VK_MODECHANGE
0x1F
IME mode change request
VK_SPACE
0x20
SPACEBAR
VK_PRIOR
0x21
PAGE UP key
VK_NEXT
0x22
PAGE DOWN key
VK_END
0x23
END key
VK_HOME
0x24
HOME key
VK_LEFT
0x25
LEFT ARROW key
VK_UP
0x26
UP ARROW key
VK_RIGHT
0x27
RIGHT ARROW key
VK_DOWN
0x28
DOWN ARROW key
VK_SELECT
0x29
SELECT key
VK_PRINT
0x2A
PRINT key
VK_EXECUTE
0x2B
EXECUTE key
VK_SNAPSHOT
0x2C
PRINT SCREEN key
VK_INSERT
0x2D
INS key
VK_DELETE
0x2E
DEL key
VK_HELP
0x2F
HELP key
0x30
0 key
0x31
1 key
0x32
2 key
0x33
3 key
0x34
4 key
0x35
5 key
0x36
6 key
0x37
7 key
0x38
8 key
0x39
9 key
-
0x3A-40
Undefined
0x41
A key
0x42
B key
0x43
C key
0x44
D key
0x45
E key
0x46
F key
0x47
G key
0x48
H key
0x49
I key
0x4A
J key
0x4B
K key
0x4C
L key
0x4D
M key
0x4E
N key
0x4F
O key
0x50
P key
0x51
Q key
0x52
R key
0x53
S key
0x54
T key
0x55
U key
0x56
V key
0x57
W key
0x58
X key
0x59
Y key
0x5A
Z key
VK_LWIN
0x5B
Left Windows key (Natural keyboard)
VK_RWIN
0x5C
Right Windows key (Natural keyboard)
VK_APPS
0x5D
Applications key (Natural keyboard)
-
0x5E
Reserved
VK_SLEEP
0x5F
Computer Sleep key
VK_NUMPAD0
0x60
Numeric keypad 0 key
VK_NUMPAD1
0x61
Numeric keypad 1 key
VK_NUMPAD2
0x62
Numeric keypad 2 key
VK_NUMPAD3
0x63
Numeric keypad 3 key
VK_NUMPAD4
0x64
Numeric keypad 4 key
VK_NUMPAD5
0x65
Numeric keypad 5 key
VK_NUMPAD6
0x66
Numeric keypad 6 key
VK_NUMPAD7
0x67
Numeric keypad 7 key
VK_NUMPAD8
0x68
Numeric keypad 8 key
VK_NUMPAD9
0x69
Numeric keypad 9 key
VK_MULTIPLY
0x6A
Multiply key
VK_ADD
0x6B
Add key
VK_SEPARATOR
0x6C
Separator key
VK_SUBTRACT
0x6D
Subtract key
VK_DECIMAL
0x6E
Decimal key
VK_DIVIDE
0x6F
Divide key
VK_F1
0x70
F1 key
VK_F2
0x71
F2 key
VK_F3
0x72
F3 key
VK_F4
0x73
F4 key
VK_F5
0x74
F5 key
VK_F6
0x75
F6 key
VK_F7
0x76
F7 key
VK_F8
0x77
F8 key
VK_F9
0x78
F9 key
VK_F10
0x79
F10 key
VK_F11
0x7A
F11 key
VK_F12
0x7B
F12 key
VK_F13
0x7C
F13 key
VK_F14
0x7D
F14 key
VK_F15
0x7E
F15 key
VK_F16
0x7F
F16 key
VK_F17
0x80
F17 key
VK_F18
0x81
F18 key
VK_F19
0x82
F19 key
VK_F20
0x83
F20 key
VK_F21
0x84
F21 key
VK_F22
0x85
F22 key
VK_F23
0x86
F23 key
VK_F24
0x87
F24 key
-
0x88-8F
Unassigned
VK_NUMLOCK
0x90
NUM LOCK key
VK_SCROLL
0x91
SCROLL LOCK key
0x92-96
OEM specific
-
0x97-9F
Unassigned
VK_LSHIFT
0xA0
Left SHIFT key
VK_RSHIFT
0xA1
Right SHIFT key
VK_LCONTROL
0xA2
Left CONTROL key
VK_RCONTROL
0xA3
Right CONTROL key
VK_LMENU
0xA4
Left MENU key
VK_RMENU
0xA5
Right MENU key
VK_BROWSER_BACK
0xA6
Browser Back key
VK_BROWSER_FORWARD
0xA7
Browser Forward key
VK_BROWSER_REFRESH
0xA8
Browser Refresh key
VK_BROWSER_STOP
0xA9
Browser Stop key
VK_BROWSER_SEARCH
0xAA
Browser Search key
VK_BROWSER_FAVORITES
0xAB
Browser Favorites key
VK_BROWSER_HOME
0xAC
Browser Start and Home key
VK_VOLUME_MUTE
0xAD
Volume Mute key
VK_VOLUME_DOWN
0xAE
Volume Down key
VK_VOLUME_UP
0xAF
Volume Up key
VK_MEDIA_NEXT_TRACK
0xB0
Next Track key
VK_MEDIA_PREV_TRACK
0xB1
Previous Track key
VK_MEDIA_STOP
0xB2
Stop Media key
VK_MEDIA_PLAY_PAUSE
0xB3
Play/Pause Media key
VK_LAUNCH_MAIL
0xB4
Start Mail key
VK_LAUNCH_MEDIA_SELECT
0xB5
Select Media key
VK_LAUNCH_APP1
0xB6
Start Application 1 key
VK_LAUNCH_APP2
0xB7
Start Application 2 key
-
0xB8-B9
Reserved
VK_OEM_1
0xBA
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the ';:' key
VK_OEM_PLUS
0xBB
For any country/region, the '+' key
VK_OEM_COMMA
0xBC
For any country/region, the ',' key
VK_OEM_MINUS
0xBD
For any country/region, the '-' key
VK_OEM_PERIOD
0xBE
For any country/region, the '.' key
VK_OEM_2
0xBF
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the '/?' key
VK_OEM_3
0xC0
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the '`~' key
-
0xC1-D7
Reserved
-
0xD8-DA
Unassigned
VK_OEM_4
0xDB
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the '[{' key
VK_OEM_5
0xDC
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the '\|' key
VK_OEM_6
0xDD
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the ']}' key
VK_OEM_7
0xDE
Used for miscellaneous characters; it can vary by keyboard.
For the US standard keyboard, the 'single-quote/double-quote' key
VK_OEM_8
0xDF
Used for miscellaneous characters; it can vary by keyboard.
-
0xE0
Reserved
0xE1
OEM specific
VK_OEM_102
0xE2
Either the angle bracket key or the backslash key on the RT 102-key keyboard
0xE3-E4
OEM specific
VK_PROCESSKEY
0xE5
IME PROCESS key
0xE6
OEM specific
VK_PACKET
0xE7
Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit
Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT,
SendInput, WM_KEYDOWN, and WM_KEYUP
-
0xE8
Unassigned
0xE9-F5
OEM specific
VK_ATTN
0xF6
Attn key
VK_CRSEL
0xF7
CrSel key
VK_EXSEL
0xF8
ExSel key
VK_EREOF
0xF9
Erase EOF key
VK_PLAY
0xFA
Play key
VK_ZOOM
0xFB
Zoom key
VK_NONAME
0xFC
Reserved
VK_PA1
0xFD
PA1 key
VK_OEM_CLEAR
0xFE
Clear key
"""

# and the note-to-freq-to-w/l table
"""
C0	 16.35	 2109.89
C#0	 17.32	 1991.47
D0	 18.35	 1879.69
D#0	 19.45	 1774.20
E0	 20.60	 1674.62
F0	 21.83	 1580.63
F#0  23.12	 1491.91
G0	 24.50	 1408.18
G#0  25.96	 1329.14
A0	 27.50	 1254.55
A#0  29.14	 1184.13
B0	 30.87	 1117.67
C1	 32.70	 1054.94
C#1  34.65	 995.73
D1	 36.71	 939.85
D#1	 38.89	 887.10
E1	 41.20	 837.31
F1	 43.65	 790.31
F#1	 46.25	 745.96
G1	 49.00	 704.09
G#1	 51.91	 664.57
A1	 55.00	 627.27
A#1	 58.27	 592.07
B1	 61.74	 558.84
C2	 65.41	 527.47
C#2	 69.30	 497.87
D2	 73.42	 469.92
D#2	 77.78	 443.55
E2	 82.41	 418.65
F2	 87.31	 395.16
F#2	 92.50	 372.98
G2	 98.00	 352.04
G#2	 103.83	 332.29
A2	 110.00	 313.64
A#2	 116.54	 296.03
B2	 123.47	 279.42
C3	 130.81	 263.74
C#3	 138.59	 248.93
D3	 146.83	 234.96
D#3	 155.56	 221.77
E3	 164.81	 209.33
F3	 174.61	 197.58
F#3	 185.00	 186.49
G3	 196.00	 176.02
G#3	 207.65	 166.14
A3	 220.00	 156.82
A#3	 233.08	 148.02
B3	 246.94	 139.71
C4	 261.63	 131.87
C#4  277.18	 124.47
D4	 293.66	 117.48
D#4  311.13	 110.89
E4	 329.63	 104.66
F4	 349.23	 98.79
F#4  369.99	 93.24
G4	 392.00	 88.01
G#4	 415.30	 83.07
A4	 440.00	 78.41
A#4	 466.16	 74.01
B4	 493.88	 69.85
C5	 523.25	 65.93
C#5/Db5 	 554.37	 62.23
D5	 587.33	 58.74
D#5/Eb5 	 622.25	 55.44
E5	 659.25	 52.33
F5	 698.46	 49.39
F#5	 739.99	 46.62
G5	 783.99	 44.01
G#5	 830.61	 41.54
A5	 880.00	 39.20
A#5	 932.33	 37.00
B5	 987.77	 34.93
C6	 1046.50	 32.97
C#6	 1108.73	 31.12
D6	 1174.66	 29.37
D#6	 1244.51	 27.72
E6	 1318.51	 26.17
F6	 1396.91	 24.70
 F#6/Gb6 	 1479.98	 23.31
G6	 1567.98	 22.00
 G#6/Ab6 	 1661.22	 20.77
A6	 1760.00	 19.60
 A#6/Bb6 	 1864.66	 18.50
B6	 1975.53	 17.46
C7	 2093.00	 16.48
 C#7/Db7 	 2217.46	 15.56
D7	 2349.32	 14.69
 D#7/Eb7 	 2489.02	 13.86
E7	 2637.02	 13.08
F7	 2793.83	 12.35
 F#7/Gb7 	 2959.96	 11.66
G7	 3135.96	 11.00
 G#7/Ab7 	 3322.44	 10.38
A7	 3520.00	 9.80
 A#7/Bb7 	 3729.31	 9.25
B7	 3951.07	 8.73
C8	 4186.01	 8.24
 C#8/Db8 	 4434.92	 7.78
D8	 4698.63	 7.34
 D#8/Eb8 	 4978.03	 6.93
E8	 5274.04	 6.54
F8	 5587.65	 6.17
 F#8/Gb8 	 5919.91	 5.83
G8	 6271.93	 5.50
 G#8/Ab8 	 6644.88	 5.19
A8	 7040.00	 4.90
 A#8/Bb8 	 7458.62	 4.63
B8	 7902.13	 4.37
"""