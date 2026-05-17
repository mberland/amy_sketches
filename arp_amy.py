import random
import amy, amyboard

chords = {
    "C": [60, 64, 67],      # C major
    "Dm": [62, 65, 69],     # D minor
    "Em": [64, 68, 71],     # E minor
    "F": [65, 69, 72],      # F major
    "G": [67, 71, 74],      # G major
    "Am": [69, 73, 76],     # A minor
    "B": [71, 75, 78]       # B major
}

progressions = [
    ["C", "Am", "F", "G"],
    ["C", "Dm", "G", "Am"],
    ["C", "F", "G", "Am"],
    ["C", "G", "Em", "C"],
    ["C", "G", "Am", "Dm"],
    ["C", "Dm", "Am", "F"],
    ["C", "G", "F", "C"],
    ["C", "F", "C", "G"],
    ["Dm", "G", "Am", "C"],
    ["Dm", "G", "C", "Am"],
    ["Dm", "Em", "C", "Dm"],
    ["Dm", "C", "G", "Dm"],
    ["F", "C", "G", "Am"],
    ["F", "G", "Am", "C"],
    ["G", "C", "Am", "F"],
    ["G", "C", "Dm", "G"],
    ["G", "Em", "C", "Dm"],
    ["G", "Am", "Dm", "G"],
    ["Am", "Dm", "G", "C"],
    ["Am", "Dm", "F", "C"],
    ["Am", "F", "C", "Dm"],
    ["Em", "C", "Dm", "G"],
    ["Em", "G", "C", "Dm"],
    ["Em", "Dm", "G", "C"],
    ["Em", "C", "Dm", "Am"]
]

step = 0
skips = 4
prog = random.choice(progressions)
chord = prog[step % len(prog)]
steps_per_bar = len(prog) * len(prog[0])
octave_mod = 0
octave_mult = 0
ticks = 0


# def do_display(s,x=0,y=0,color=255):
#     amyboard.display.fill(0)    
#     amyboard.display.text(s, x, y, color)
#     amyboard.display_refresh()

def draw_line(x1, y1, x2, y2, color=255):
    amyboard.display.line(x1, y1, x2, y2, color)

def clamp(x, min_val, max_val):
    return max(min(x, max_val), min_val)

# MIDI note 60 is C4 = 0V
# octave is 12 semitones
def midi_to_oct_cv(note):
    return clamp((note - 60.0) / 12.0, -5.0, 5.0)



def loop():
    global step, prog, chord, steps_per_bar, ticks, octave_mod, octave_mult
    ticks += 1
    if 0 == ticks % (skips // 2):
        amyboard.cv_out(0.0, channel=1)
    if 0 == ticks % skips:
        
        step += 1
        if (random.random() < 0.25):
            amy.send(synth=1, vel=0)
        
        octave_mult = random.randint(0,2)
        octave_mod = -12 * octave_mult

        if 0 == step % (4 * steps_per_bar):
            amy.send(synth=1, vel=0)
            prog = random.choice(progressions)

        chord = prog[(step // 4) % len(prog)]
        chord_notes = chords[chord]
        note = chord_notes[step % 4] + octave_mod
        amyboard.cv_out(midi_to_oct_cv(note), channel=0)
        amyboard.cv_out(5.0, channel=1)
        amy.send(synth=1, note=note, vel=0.9)

        amyboard.display.fill(0)
        prog_str = prog[0] + f"{4-octave_mult} : "  + " : ".join(prog[1:])
        amyboard.display.text(prog_str, 0, 0, 255)
        amyboard.display.text(f"{note} ({midi_to_oct_cv(note):.2f}V)", 0, 20, 255)
        amyboard.display_refresh()
        
