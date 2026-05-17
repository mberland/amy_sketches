import amyboard, amy, sequencer
from music import Chord, Key, Progression
import time, random



amy.send(synth=1, num_voices=1, patch=100)

PROGRESSIONS = [
    ["i", "VI", "III", "VII"],   # Am F C G  (classic house)
    ["i", "iv", "VI", "VII"],    # Am Dm F G
    ["i", "III", "VII", "VI"],   # Am C G F
    ["i", "VII", "VI", "VII"],   # Am G F G
]
KEY = Key("A:min")

prog = Progression(random.choice(PROGRESSIONS), KEY)
chords = prog.chords


STEPS_PER_BAR = 32
BARS_PER_CHORD = 4
STEPS_PER_CHORD = STEPS_PER_BAR * BARS_PER_CHORD
TOTAL_STEPS = STEPS_PER_CHORD * len(chords)


step = 0


def loop():
    global step, chords, prog
    step += 1
    if step < 5:
        return
    if 0 == step % STEPS_PER_BAR:
        prog = Progression(random.choice(PROGRESSIONS), KEY)
        chords = prog.chords
        update = True
    else:
        update = False
        
    chord_idx = step % len(chords)
    chord = chords[chord_idx]
    print(chord)
    root_midi = chord.notes[0]
    print(root_midi)
    fifth_midi = root_midi + 7
    octave_midi = root_midi + 12
    notes = [root_midi, fifth_midi, octave_midi]
    note = notes[step % len(notes)]
    amy.send(synth=1, note=note, vel=0)
    amy.send(synth=1, note=note, vel=0.9)

    if update:
        amyboard.display.fill(0)
        amyboard.display.text(chord.root_note.name(), 0, 0, 255)
        amyboard.display.text(">"+chords[0].root_note.name(), 0, 24, 255)
        amyboard.display_refresh()
