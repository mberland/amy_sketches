import random, amyboard, time, sequencer, amy

chords = {
    "C": [60, 64, 67], "Dm": [62, 65, 69],
    "Em": [64, 68, 71], "F": [65, 69, 72], 
    "G": [67, 71, 74], "Am": [69, 73, 76], 
    "B": [71, 75, 78]
}

progressions = [
    ["Am", "Dm", "G", "C"],
    ["Am", "Dm", "F", "C"],
    ["Am", "F", "C", "Dm"],
    ["Em", "C", "Dm", "G"],
    ["Em", "G", "C", "Dm"],
    ["Em", "Dm", "G", "C"],
    ["Em", "C", "Dm", "Am"]
]

def amy_clamp(x, min_val, max_val):
    return max(min(x, max_val), min_val)

def midi_to_oct_cv(note):
    return amy_clamp((note - 60.0) / 12.0, -5.0, 5.0)

def oct_cv_to_midi(cv):
    return int(60 + 12.0 * amy_clamp(cv, -5.0, 5.0))

def quantize_cv(cv):
    return midi_to_oct_cv(oct_cv_to_midi(cv))

def amy_shuffle(xs):
    return sorted(xs, key=lambda x: random.random())

last_encoder = -1

HISTORY_LENGTH = 50
X_MAX = 83
X_BUF = 4

history_scale = 100.0

calibration_max = 1.0
calibration_min = -1.0

def randmax():
    if random.random() < 0.5:
        return 10
    return -10

cv1history = [randmax() for _ in range(HISTORY_LENGTH)]
cv2history = [randmax() for _ in range(HISTORY_LENGTH)]
X_MULT = 125.0 / HISTORY_LENGTH


def draw_graph(data, y_min=15, y_max=85):
    global X_MAX, X_BUF, X_MULT
    hist_min = min(data)
    hist_max = max(data)
    if hist_max - hist_min < 2:
        return False
    hist_range = 1.0 * max(1, hist_max - hist_min)
    amyboard.display.text(f"{hist_max/history_scale:+.1f}",round(X_MAX+X_BUF+1),y_min+5,255)
    amyboard.display.text(f"{hist_min/history_scale:+.1f}",round(X_MAX+X_BUF+1),y_max-15,255)

    for i in range(len(data) - 1):
        x1 = X_BUF + int(i*X_MULT)
        x2 = x1 + 2
        y1 = y_min + int((y_max-y_min) * (data[i] - hist_min) / hist_range)
        y2 = y_min + int((y_max-y_min) * (data[i+1] - hist_min) / hist_range)
        amyboard.display.line(x1,y1,x2,y2,255)
    return True

last_encoder = -99
def check_encoder():
    global last_encoder
    current_encoder = amyboard.read_encoder(encoder=0, seesaw_dev=54)
    if last_encoder != current_encoder:
        change_progression()
        bpm = sequencer.tempo()
        if last_encoder > current_encoder:
            bpm = min(300, bpm + 20)
        else:
            bpm = max(20, bpm - 20)
        last_encoder = current_encoder
        sequencer.tempo(bpm)    

cv1prog = random.choice(progressions)
cv2prog = random.choice(progressions)
def change_progression():
    global cv1prog, cv2prog
    cv1prog = random.choice(progressions)
    cv2prog = random.choice(progressions)


def generate_note(prog,step,octave):    
    chord_num = step % len(prog)
    chord = prog[chord_num]
    chord_notes = chords[chord]
    octave_mod = (octave - 4) * 12
    note = chord_notes[step % len(chord_notes)] + octave_mod
    return midi_to_oct_cv(note)

last_note = None

def update_scope():
    global cv1history, cv2history, skips, ticks, last_encoder, is_audio, last_note
    amyboard.display.fill(0)
    amyboard.display.text(f"SCOPE: {sequencer.tempo()} BPM",2,5,255)

    amyboard.display.line(0,15,128,15,255)
    if draw_graph(cv1history,18,68):
        amyboard.cv_out(quantize_cv(cv1), channel=0)
    else:
        prog_str = cv1prog[0] + f"3 "  + " ".join(cv1prog[1:])
        amyboard.display.text("~> " + prog_str, 2, 40, 255)
        note = generate_note(cv1prog,ticks//skips,3)
        amyboard.cv_out(note, channel=0)
        if is_audio and note != last_note:
            amy.send(synth=1, vel=0)
            amy.send(synth=1, note=oct_cv_to_midi(note), vel=1)
        last_note = note
    
    amyboard.display.line(0,70,128,70,255)
    if draw_graph(cv2history,75,125):
        amyboard.cv_out(quantize_cv(cv2), channel=1)
    else:
        prog_str = cv2prog[0] + f"2 "  + " ".join(cv2prog[1:])
        amyboard.display.text("~> " + prog_str, 2, 90, 255)
        note = generate_note(cv2prog,ticks//skips,2)
        amyboard.cv_out(note, channel=1)
        if is_audio and note != last_note:
            amy.send(synth=1, vel=0)
            amy.send(synth=1, note=oct_cv_to_midi(note), vel=1)
        last_note = note

    amyboard.display_refresh()

cv1 = 0.0
cv2 = 0.0

sequencer.tempo(120)

ctime = time.time()
last_time = ctime
step = 0
skips = 4
ticks = 0

amy.send(synth=1, patch=100)
is_audio = True

def loop():
    global cv1, cv2, cv1history, cv2history, last_time, ctime, ticks
    ticks += 1

    cv1 = amyboard.cv_in(channel=0)
    time.sleep(0.05)
    cv2 = amyboard.cv_in(channel=1)
    time.sleep(0.05)
    
    if cv1 < -8 or cv1 > 8:
        cv1 = 0.0
    if cv2 < -8 or cv2 > 8:
        cv2 = 0.0
    cv1history.append(int(history_scale * cv1))
    cv1history.remove(cv1history[0])
    cv2history.append(int(history_scale * cv2))
    cv2history.remove(cv2history[0])

    check_encoder()
    update_scope()