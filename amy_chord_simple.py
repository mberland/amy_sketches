# AMYboard Sketch
# DESCRIPTION: Four-chord arpeggio sequencer. Default 120 BPM
# internal clock; gate pulses >2.5V on CV1 override the step clock. Audio on patch 100
# plus 1V/oct CV out on CV1. Display shows BPM, chord progression, and active chord.

import amy, amyboard, tulip, time, sequencer, random
from music import Chord

# --- Synth setup ---
amy.send(synth=1, patch=100, num_voices=6, grab_midi_notes=0)
amy.send(reverb="0.5,0.4,0.08")

# --- Chord progressions ---
CHORD_PROGRESSIONS = [
    ["A:min", "D:min", "G:maj", "C:maj"],
    ["A:min", "D:min", "F:maj", "C:maj"],
    ["A:min", "F:maj", "C:maj", "D:min"],
    ["E:min", "C:maj", "D:min", "G:maj"],
    ["E:min", "G:maj", "C:maj", "D:min"],
    ["E:min", "D:min", "G:maj", "C:maj"],
    ["E:min", "C:maj", "D:min", "A:min"]
]

prog_idx = random.randint(0,len(CHORD_PROGRESSIONS) - 1)

def build_chord_notes(chord_str, octave=4):
    c = Chord(chord_str)
    base = c.midinotes(octave=octave)
    return base + [base[0] + 12]

def build_chord_for_prog():    
    global prog_idx, CHORD_PROGRESSIONS
    prog_idx %= len(CHORD_PROGRESSIONS)
    return [build_chord_notes(name) for name in CHORD_PROGRESSIONS[prog_idx]]

CHORDS = build_chord_for_prog()

note_name_from_chord = lambda chord_str: chord_str[0]

def is_external_clock():
    global now
    now = time.time()
    return len(gate_times) >= 1 and (now - gate_times[-1]) < 5
     

# --- Timing ---
DEFAULT_BPM = 120
current_bpm = DEFAULT_BPM
amy.send(tempo=current_bpm)
now = time.time()

# --- State ---
chord_idx = 0
arp_step = 0
notes_per_chord = 8
note_count = 0
last_note = None
last_gate = False
gate_times = []
MAX_GATE_TIMES = 8

# --- Display ---
amyboard.init_display()


def update_display():
    global current_bpm, chord_idx, arp_step, note_count, now
    label_xs = [0, 24, 48, 72]
    if chord_idx == 0:
        amyboard.display.fill(0)
        amyboard.display.text("CV ARPEGGIO", 0, 0, 255)
        bpm_str = "BPM:" + str(current_bpm)
        amyboard.display.text(bpm_str, 0, 14, 220)        
        recent_ext = is_external_clock()
        src = "EXT" if recent_ext else "INT"
        amyboard.display.text("CLK:" + src, 0, 84, 180)
        for i in range(len(CHORD_PROGRESSIONS[prog_idx])):
            col = 255 if i == chord_idx else 140
            amyboard.display.text(note_name_from_chord(CHORD_PROGRESSIONS[prog_idx][i]), label_xs[i], 30, col)
    arrow_x = label_xs[chord_idx]
    amyboard.display.text("^", arrow_x, 42, 255)
    amyboard.display_refresh()

def note_on_for_step():
    global arp_step, last_note, note_count, chord_idx
    CHORDS = build_chord_for_prog()
    notes = CHORDS[chord_idx]
    midi_note = notes[arp_step % len(notes)]
    if last_note is not None:
        amy.send(synth=1, note=last_note, vel=0)
    amy.send(synth=1, note=midi_note, vel=0.85)
    last_note = midi_note
#    cv_volts = (midi_note - 60) / 12.0
#    amyboard.cv_out(cv_volts, channel=0)
    arp_step += 1
    note_count += 1
    if note_count >= notes_per_chord:
        note_count = 0
        chord_idx = (chord_idx + 1) % len(CHORDS)
        arp_step = 0
        update_display()

def compute_bpm_from_gates():
    global current_bpm
    if len(gate_times) < 2:
        return
    intervals = []
    for i in range(1, len(gate_times)):
        intervals.append(gate_times[i] - gate_times[i - 1])
    if not intervals:
        return
    avg_secs = abs(sum(intervals) / len(intervals))
    if avg_secs > 0:
        new_bpm = int(60.0 / avg_secs)
        new_bpm = max(40, min(300, new_bpm))
        current_bpm = new_bpm
        amy.send(tempo=current_bpm)
#    print(f"new = {new_bpm}, curr = {current_bpm}: {gate_times}, intervals = {intervals}, avg_secs = {avg_secs}")
    update_display()
    
update_display()
last_ext = -1
ticks = 0

def loop():
    global last_gate, gate_times, now, prog_idx, current_bpm, last_ext, notes_per_chord, ticks
    ticks += 1
    
    now = time.time()
    cv_v = amyboard.cv_in(0)
    gate_high = cv_v > 2.5

    if gate_high and not last_gate:
        gate_times.append(now)
        if len(gate_times) > MAX_GATE_TIMES:
            gate_times = gate_times[-MAX_GATE_TIMES:]
        compute_bpm_from_gates()
    elif not gate_high and last_gate:
        if last_note is not None:
            amy.send(synth=1, note=last_note, vel=0)

    last_gate = gate_high

    recent_ext = is_external_clock()
    if recent_ext != last_ext:
        prog_idx = random.randint(0,len(CHORD_PROGRESSIONS))
    last_ext = recent_ext

    if 0 == ticks % notes_per_chord:
        note_on_for_step()
        update_display()