import random, amyboard, time, sequencer


def amy_clamp(x, min_val, max_val):
    return max(min(x, max_val), min_val)

def midi_to_oct_cv(note):
    return amy_clamp((note - 60.0) / 12.0, -5.0, 5.0)

def oct_cv_to_midi(cv):
    return int(60 + 12 * amy_clamp(cv, -5.0, 5.0))

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

history = [(randmax(),randmax()) for _ in range(HISTORY_LENGTH)]
X_MULT = 125.0 / HISTORY_LENGTH


def draw_graphs(data):
    global X_MAX, X_BUF, X_MULT
    cv1_data = [d[0] for d in data]
    cv2_data = [d[1] for d in data]
    all_data = cv1_data + cv2_data
    hist_min = min(all_data)
    hist_max = max(all_data)
    hist_range = max(1, hist_max - hist_min)
    cv1_scaled = [(d - hist_min) / (hist_range) for d in cv1_data]
    cv2_scaled = [(d - hist_min) / (hist_range) for d in cv2_data]
    y_size = 45.0
    cv1y_min = 15    
    cv2y_min = int(cv1y_min + y_size)
    y_bottom = 128-20
    amyboard.display.text(f"SCOPE",2,5,255)
    amyboard.display.line(0,cv1y_min - 1,128,cv1y_min - 1,255)
    amyboard.display.line(0,cv2y_min,128,cv2y_min,255)
    amyboard.display.line(0,y_bottom,128,y_bottom,255)
    amyboard.display.text(f"{hist_min/history_scale:+.1f} >> {hist_max/history_scale:+.1f}",2,y_bottom+5,255)

    for i in range(len(data) - 1):
        x1 = X_BUF + int(i*X_MULT)
        x2 = x1 + 2
        
        if hist_range < 2:
            amyboard.display.text("NO DATA", 2, 70, 255)
        else:
            cv1y1 = cv1y_min + int(y_size * cv1_scaled[i])
            cv1y2 = cv1y_min + int(y_size * cv1_scaled[i+1])
            cv2y1 = cv2y_min + int(y_size * cv2_scaled[i])
            cv2y2 = cv2y_min + int(y_size * cv2_scaled[i+1])
            amyboard.display.line(x1,cv1y1,x2,cv1y2,255)
            amyboard.display.line(x1,cv2y1,x2,cv2y2,255)
    amyboard.display.refresh()


def update_display():
    global history
    amyboard.display.fill(0)
    draw_graphs(history)
    amyboard.display_refresh()

cv1 = 0.0
cv2 = 0.0
update_display()

sequencer.tempo(60)

ctime = time.time()
last_time = ctime
step = 0
skips = 4
ticks = 0

def loop():
    global cv1, cv2, history, last_time, ctime, ticks
    ticks += 1
    cv1out = midi_to_oct_cv(oct_cv_to_midi(cv1))
    cv2out = midi_to_oct_cv(oct_cv_to_midi(cv2))
    amyboard.cv_out(channel=0, value=cv1out)
    amyboard.cv_out(channel=1, value=cv2out)
    if 0 == ticks % 2:
        cv1 = amyboard.cv_in(channel=0)
    else:
        cv2 = amyboard.cv_in(channel=1)	
    history.append((int(history_scale * cv2),int(history_scale * cv1)))
    history.remove(history[0])
    update_display()