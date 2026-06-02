import random, amyboard, sequencer, time

#scales = { "major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10] }
#intervals = {"dim": [0, 3, 6],"min": [0, 3, 7],"maj": [0, 4, 7],"sus": [0, 5, 7]}
#extensions = {"6": 9, "m7": 10, "M7": 11, "9": 14}

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

def amy_shuffle(xs):
    return sorted(xs, key=lambda x: random.random())

step = 0
skips = 4
prog = random.choice(progressions)
chord = prog[step % len(prog)]
steps_per_bar = 4 * len(prog) * len(prog[0])
octave_mod = 0
octave_mult = 0
ticks = 0
gate_time = 0.5
gate_start = -1.0
last_encoder = -1

sequencer.tempo(120)

HISTORY_LENGTH = 30
X_MAX = 90.0
X_BUF = 4

    

history = [random.randint(40, 80) for _ in range(HISTORY_LENGTH)]
X_MULT = X_MAX / HISTORY_LENGTH


def draw_graph(data, y_mid=100, y_size=0.4):
    global X_MAX, X_BUF, X_MULT
    y_min = y_mid + (y_size // 2)
    hist_min = min(data)
    hist_max = max(data)
    hist_range = 1.0 * max(1, hist_max - hist_min)
    val = (data[0] - hist_min) / hist_range
    amyboard.display.text(f"{midi_to_oct_cv(hist_max):+.1f}",round(X_MAX+X_BUF+1),y_mid-y_size//2,255)
    amyboard.display.text(f"{midi_to_oct_cv(hist_min):+.1f}",round(X_MAX+X_BUF+1),y_mid+(y_size//2)-5,255)
    for i in range(len(data)):
        x1 = X_BUF + round(i*X_MULT)
        x2 = x1 + 2
        if (hist_max - hist_min) < 1:
            y1 = y_mid
            y2 = y_mid
        else:
            last_val = val
            val = (data[i] - hist_min) / hist_range
            y1 = y_min - int(y_size * last_val)
            y2 = y_min - int(y_size * val)
        amyboard.display.line(x1,y1,x2,y2,255)
    amyboard.display.refresh()

#def enqueue(data,val):
#    data = data[1:] + [val]
#    return data

def update_display():
    global history, octave_mult, prog
    amyboard.display.fill(0)
    prog_str = prog[0] + f"{4-octave_mult} "  + " ".join(prog[1:])
    amyboard.display.text("~> " + prog_str, 2, 5, 255)
    amyboard.display.text(f"enc {amyboard.read_encoder(encoder=0, seesaw_dev=54)}", 2, 15, 255)    
    amyboard.display.text(f"tempo {sequencer.tempo():.0f}",2,25,255)
    beat_string = ""
    if btoggle:
        beat_string = "XXXXXXXXXXXX"
    draw_graph(history,110,27)
    amyboard.display.text(beat_string, 2, 35, 255)
    amyboard.display_refresh()


def fix_tempo():
    global gate_start, gate_time
    cv2 = amyboard.cv_in(channel=1)
    if cv2 > 2.5:
        if gate_start < 0:
            gate_start = time.time()
    elif gate_start > 0:
        gate_time = time.time() - gate_start
        gate_start = -1.0
    if gate_time > 0.01:
        sequencer.tempo(60.0 / gate_time)
    

def switch_prog():
    global prog, progressions, octave_mult, octave_mod
    prog = random.choice(progressions)
    octave_mult = random.randint(0,2)
    octave_mod = -12 * octave_mult

chord_num = -1
btoggle = False

def loop():
    global step, prog, chord, chord_num, steps_per_bar, ticks, octave_mod, octave_mult, history, last_encoder, btoggle
    ticks += 1
    fix_tempo()
    if 0 == ticks % (skips // 2):
        amyboard.cv_out(0, channel=1)
        btoggle = not btoggle
    if 0 == ticks % skips:
        update_display()
        step += 1
        current_encoder = amyboard.read_encoder(encoder=0, seesaw_dev=54)
        if last_encoder != current_encoder:
            last_encoder = current_encoder
            switch_prog()
        chord_num = (step // 4) % len(prog)
        chord = prog[chord_num]
        chord_notes = chords[chord]
        note = chord_notes[step % len(chord_notes)] + octave_mod
        amyboard.cv_out(midi_to_oct_cv(note), channel=0)
        amyboard.cv_out(5.0, channel=1)
        btoggle = not btoggle
        history.append(note)
        history.remove(history[0])