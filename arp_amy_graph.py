import random, amy, amyboard, sequencer, time

scales = { "major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10] }
intervals = {"dim": [0, 3, 6],"min": [0, 3, 7],"maj": [0, 4, 7],"sus": [0, 5, 7]}
extensions = {"6": 9, "m7": 10, "M7": 11, "9": 14}

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
last_encoder = -1

random_patch = random.randint(1,255)
amy.reverb(0.5)
amy.echo(level=0.3, delay_ms=200, feedback=0.8)
sequencer.tempo(120)

HISTORY_LENGTH = 30
X_MAX = 90.0
X_BUF = 4

    

history = [random.random() for _ in range(HISTORY_LENGTH)]
#cv1s = [0.0 for _ in range(HISTORY_LENGTH)]
X_MULT = X_MAX / HISTORY_LENGTH


def draw_graph(data, y_mid=100, y_size=40):
    global X_MAX, X_BUF, X_MULT
    y_min = y_mid + (y_size // 2)
    hist_min: float = min(data)
    hist_max: float = max(data)
    hist_range: float = max(0.1, hist_max - hist_min)
    val = (data[0] - hist_min) / hist_range
    amyboard.display.text(f"{hist_max:+.1f}",round(X_MAX+X_BUF+1),y_mid-y_size//2,255)
    amyboard.display.text(f"{hist_min:+.1f}",round(X_MAX+X_BUF+1),y_mid+(y_size//2)-5,255)
    for i in range(len(data)):
        x1 = X_BUF + round(i*X_MULT)
        x2 = x1 + 2
        if (hist_max - hist_min) < 0.01:
            y1 = y_mid
            y2 = y_mid
        else:
            last_val = val
            val = (data[i] - hist_min) / hist_range
            y1 = y_min - int(y_size * last_val)
            y2 = y_min - int(y_size * val)
        amyboard.display.line(x1,y1,x2,y2,255)
    amyboard.display.refresh()

def enqueue(data,val):
    data = data[1:] + [val]
    return data

def update_display():
    global cv1s, history, octave_mult, prog
    amyboard.display.fill(0)
    prog_str = prog[0] + f"{4-octave_mult} "  + " ".join(prog[1:])
    amyboard.display.text("~> " + prog_str, 2, 5, 255)
    amyboard.display.text(f"enc {amyboard.read_encoder(encoder=0)}", 2, 15, 255)    
    #amyboard.display.text(f"patch {random_patch}", 2, 15, 255)
    #amyboard.display.text(f"   cv {amyboard.cv_in(channel=0):.1f} {amyboard.cv_in(channel=1):.1f}",2,25,255)
    amyboard.display.text(f"tempo {sequencer.tempo():.0f}",2,35,255)
    #draw_graph(cv1s,75,27)
    draw_graph(history,110,27)
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
    sequencer.tempo(60.0 / gate_time)
    

def switch_prog():
    global step, prog, chord, steps_per_bar, ticks, octave_mod, octave_mult, history, random_patch
    amy.send(synth=1, vel=0)
    random_patch = random.randint(1,255)
    prog = random.choice(progressions)
    octave_mult = random.randint(0,2)
    octave_mod = -12 * octave_mult
#    prog = amy_shuffle(prog)

chord_num = -1
#amy.send(patch=131, voices=[0,1,2])
#amy.send(patch=131, voices=[1])

amy.send(synth=1, patch=1)     # 4 voices of Juno patch #1 on synth 1
amy.send(synth=2, patch=129)   # 4 voices of DX7 patch #2 on synth 2
#amy.send(synth=1, osc=0, filter_freq=8000)   # Open up the filter on the Juno voices


def loop():
    global step, prog, chord, chord_num, steps_per_bar, ticks, octave_mod, octave_mult, history, random_patch, last_encoder, cv1s
    ticks += 1
    fix_tempo()
    if 0 == ticks % (skips * 2):
        update_display()
    if 0 == ticks % skips:
        step += 1
        current_encoder = amyboard.read_encoder(encoder=0)
        if last_encoder != current_encoder:
            last_encoder = current_encoder
            amyboard.set_neopixel(0, random.randint(0, 128), random.randint(0, 128), random.randint(0, 128))
            amyboard.show_neopixels()
            switch_prog()
        if chord_num != (step // 4) % len(prog):
            chord_num = (step // 4) % len(prog)
            if (random.random() < 0.5):
                amy.send(synth=1, vel=0)
            if (random.random() < 0.5):
                amy.send(synth=2, vel=0)
        chord = prog[chord_num]
        chord_notes = chords[chord]
        note = chord_notes[step % len(chord_notes)] + octave_mod
        for i in range(len(chord_notes)):
            if (random.random() < 0.5):
            	amy.send(vel=0.5, synth=1, note=chord_notes[i])
            if (random.random() < 0.5):
                amy.send(vel=0.5, synth=2, note=chord_notes[i])

#        amyboard.cv_out(midi_to_oct_cv(note), channel=0)
#        amyboard.cv_out(5.0, channel=1)
#        amy.send(synth=1, note=note, vel=0.9, voices=[0,1])
        
        history = enqueue(history, midi_to_oct_cv(note))
#        cv1s = enqueue(cv1s, amyboard.cv_in(channel=0))
        

# Do not edit. Set automatically by the knobs on AMYboard Online.
_auto_generated_knobs = """
i1ic255Z
i1iv4in6Z
i1v0w20a0.591F7999.999,0.661,,2.252R1.015c2L1G4A518,,83561,0.299,310,0.000Z
i1v1w4a,,0.000f0.609A148,,10000,Z
i1v2w1a0.000,,0.000,0.000d0.720c3L1Z
i1v3w3a,,0.000,0.000c4L1Z
i1v4w1a0.551,,0.000,0.000f220.000c5L1Z
i1v5w5a0.000,,0.000,0.000L1Z
i1V1.000x7.000,-3.000,-3.000M0.300,200.000,,0.800,0.000k1.000,320.000,0.500,0.500h0.500,0.850,0.500,3000.000Z
i2ic255Z
i2iv4in8Z
i2v0w8a,,,0.000f,,,1.000b0.160L1o22O2,3,4,5,6,7A,,,1.000,0,1.000,0,1.000,731,1.000T2X3Z
i2v1a,,0.000f6.167P0.250Z
i2v2a0.386,,0.000P0.250I0.500L1A,0.000,,1.000,21,0.917,484,0.386,48,0.000T2Z
i2v3a2.000,,0.000P0.250I0.501L1A,0.000,,1.000,21,0.917,822,0.210,44,0.000T2Z
i2v4a2.000,,0.000P0.250I0.499L1A,0.000,,1.000,21,0.917,822,0.210,44,0.000T2Z
i2v5a2.000,,0.000P0.250I0.498L1A,0.000,,1.000,21,0.917,822,0.210,44,0.000T2Z
i2v6a0.545,,0.000P0.250I0.504L1A,0.000,,1.000,21,0.917,871,0.193,43,0.000T2Z
i2v7a2.000,,0.000P0.250I0.504L1A,0.000,,1.000,21,0.917,871,0.193,43,0.000T2Z
"""
