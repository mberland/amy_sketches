import random, amy, amyboard, sequencer, time

chords = {
    "C": [60, 64, 67], "Dm": [62, 65, 69],
    "Em": [64, 68, 71], "F": [65, 69, 72], 
    "G": [67, 71, 74], "Am": [69, 73, 76], 
    "B": [71, 75, 78]
}

progressions = [
    # ["C", "Am", "F", "G"],
    # ["C", "Dm", "G", "Am"],
    # ["C", "F", "G", "Am"],
    # ["C", "G", "Em", "C"],
    # ["C", "G", "Am", "Dm"],
    # ["C", "Dm", "Am", "F"],
    # ["C", "G", "F", "C"],
    # ["C", "F", "C", "G"],
    # ["Dm", "G", "Am", "C"],
    # ["Dm", "G", "C", "Am"],
    # ["Dm", "Em", "C", "Dm"],
    # ["Dm", "C", "G", "Dm"],
    # ["F", "C", "G", "Am"],
    # ["F", "G", "Am", "C"],
    # ["G", "C", "Am", "F"],
    # ["G", "C", "Dm", "G"],
    # ["G", "Em", "C", "Dm"],
    # ["G", "Am", "Dm", "G"],
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

# MIDI note 60 is C4 = 0V
# octave is 12 semitones
def midi_to_oct_cv(note):
    return amy_clamp((note - 60.0) / 12.0, -5.0, 5.0)

def amy_shuffle(xs):
    return sorted(xs, key=lambda x: random.random())

step = 0
skips = 4
prog = amy_shuffle(random.choice(progressions))
chord = prog[step % len(prog)]
steps_per_bar = 4 * len(prog) * len(prog[0])
octave_mod = 0
octave_mult = 0
ticks = 0
gate_time = 0.5
gate_start = -1.0

random_patch = random.randint(1,255)
amy.reverb(1)
amy.echo(level=0.5, delay_ms=100, feedback=0.8)
sequencer.tempo(120)

HISTORY_LENGTH = 40
X_MAX = 155
X_BUF = 4
Y_BUF = 100
X_MULT = 3
Y_MULT = 4
history = [random.random() for _ in range(HISTORY_LENGTH)]

def draw_history():
    global history
    X_MULT = X_MAX // len(history)
    y_min = min(history)
    y_max = max(history)
    y_diff = y_max-y_min
    Y_MULT = 40 // max(1,y_diff)
    Y_BUF = 125 - abs(int(y_min * Y_MULT))
    val = 0
    amyboard.display.text(f"MAX {y_max:+.1f}",4,50,255)
    amyboard.display.text(f"MIN {y_min:+.1f}",4,60,255)
    amyboard.display.text(f"{history[-1]:+.1f}",85,55,255)
    for i in range(len(history)):
        last_val = val
        val = history[i]
        x1 = X_BUF + i*X_MULT
        x2 = x1 + 2
        y1 = Y_BUF - int(Y_MULT * last_val)
        y2 = Y_BUF - int(Y_MULT * val)
        amyboard.display.line(x1,y1,x2,y2,255)
    amyboard.display.refresh()

def add_history(val):
    global history
    history = history[1:] + [val]


def fix_tempo():
    global gate_start, gate_time
    cv2 = amyboard.cv_in(channel=1)
    if cv2 > 2.5:
        if gate_start < 0:
            gate_start = time.time()
            print(gate_start)
    elif gate_start > 0:
        gate_time = time.time() - gate_start
        gate_start = -1.0
    sequencer.tempo(60.0 / gate_time)
    


def loop():
    global step, prog, chord, steps_per_bar, ticks, octave_mod, octave_mult, history, random_patch
    ticks += 1
    fix_tempo()
#    if 0 == ticks % (skips // 2):
#        amyboard.cv_out(0.0, channel=1)
    if 0 == ticks % skips:
        
        step += 1
#        if (random.random() < 0.25):
#            amy.send(synth=1, vel=0)

        if 0 == step % (4 * steps_per_bar):
            amy.send(synth=1, vel=0)
            random_patch = random.randint(1,255)
            prog = random.choice(progressions)
            octave_mult = random.randint(0,2)
            octave_mod = -12 * octave_mult
            prog = amy_shuffle(prog)

        chord = prog[(step // 4) % len(prog)]
        chord_notes = chords[chord]
        note = chord_notes[step % len(chord_notes)] + octave_mod
#        amyboard.cv_out(midi_to_oct_cv(note), channel=0)
#        amyboard.cv_out(5.0, channel=1)
        amy.send(synth=1, patch=random_patch, note=note, vel=0.9)

        amyboard.display.fill(0)
        prog_str = prog[0] + f"{4-octave_mult} "  + " ".join(prog[1:])
        amyboard.display.text(prog_str, 2, 5, 255)
        amyboard.display.text(f"patch {random_patch}", 2, 15, 255)
        amyboard.display.text(f"   cv {amyboard.cv_in(channel=0):.1f} {amyboard.cv_in(channel=1):.1f}",2,25,255)
        amyboard.display.text(f"tempo {sequencer.tempo():.0f}",2,35,255)
        
        add_history(midi_to_oct_cv(note))
        draw_history()
        amyboard.display_refresh()
