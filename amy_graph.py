import random, amy, amyboard


amyboard.display.fill(0)
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
    Y_MULT = 40 // max(10,y_diff)
    Y_BUF = 100
    val = 0
    amyboard.display.text(f"MAX {y_max:+.1f}",4,50,255)
    amyboard.display.text(f"MIN {y_min:+.1f}",4,60,255)
    amyboard.display.text(f"{history[-1]:+.1f}",85,55,255)
    for i in range(len(history)):
        last_val = val
        val = history[i]
        x1 = X_BUF + i*X_MULT
        x2 = x1 + 2
        y1 = Y_BUF + int(Y_MULT * last_val)
        y2 = Y_BUF + int(Y_MULT * val)
        amyboard.display.line(x1,y1,x2,y2,255)
    amyboard.display.refresh()

def add_history(val):
    global history
    history = history[1:] + [val]

ticks = 0
def loop():    
    global history, ticks
    amyboard.display.fill(0)

    if (random.random() < 0.95):
        r = 5.0*(random.random()-0.5)
        add_history(r)
    else:
        r = 10.0*(random.random()-0.5)
        add_history(r)
    if (0 == ticks % 2):
        draw_history()
    ticks += 1
    pass

# Do not edit. Set automatically by the knobs on AMYboard Online.
_auto_generated_knobs = """
i1ic255Z
i1iv6in4Z
i1v0w20F286.612,1.000,,,5.000R2.356c2L1G4A96,,1000,0.200,124,0.000B149,1.000,1000,0.778,873,0.000Z
i1v1a,,0.000f4.000,0.000,,,,,0.000A,,10000,Z
i1v2w1a,,0.000,0.000f219.334,,,,,0.025c3L1Z
i1v3w3a,,0.000,0.000f220.000,,,,,0.025L1Z
i1V1.000x0.000,0.000,0.000M0.305,392.948,,0.547,0.000k0.633,320.000,0.500,0.500h0.512,0.850,0.500,3000.000Z
"""
