import random, amyboard, time, sequencer


def amy_clamp(x, min_val, max_val):
    return max(min(x, max_val), min_val)

def midi_to_oct_cv(note):
    return amy_clamp((note - 60.0) / 12.0, -5.0, 5.0)

def amy_shuffle(xs):
    return sorted(xs, key=lambda x: random.random())

step = 0
skips = 4
ticks = 0
last_encoder = -1

HISTORY_LENGTH = 30
X_MAX = 83
X_BUF = 4



history = [(random.randint(-10,10),random.randint(-10,10)) for _ in range(HISTORY_LENGTH)]
X_MULT = 120 / HISTORY_LENGTH


def draw_graph(data, y_mid=100, y_size=45):
    global X_MAX, X_BUF, X_MULT
    y_min = y_mid + (y_size // 2)
    hist_min = min(data)
    hist_max = max(data)
    hist_range = 1.0 * max(1, hist_max - hist_min)
    val = (data[0] - hist_min) / hist_range
    amyboard.display.text(f"{hist_max:+.1f}",X_BUF,y_mid-y_size//2,255)
    amyboard.display.text(f"{hist_min:+.1f}",X_BUF,y_mid+(y_size//2)-5,255)
    for i in range(len(data)):
        x1 = X_BUF + int(i*X_MULT)
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


def update_display():
    global history
    amyboard.display.fill(0)
    amyboard.display.text("CPL SCOPE", 2, 5, 255)
    cv1s = map(lambda x: x[0], history)
    cv2s = map(lambda x: x[1], history)
    draw_graph(list(cv1s),43,48)
    amyboard.display.line(0,15,128,15,255)
    amyboard.display.line(0,70,128,70,255)
    draw_graph(list(cv2s),98,48)
    amyboard.display_refresh()

cv1 = 0.0
cv2 = 0.0
update_display()

sequencer.tempo(30)

ctime = time.time()
last_time = ctime

def loop():
    global cv1, cv2, history, last_time, ctime
    last_time = ctime
    ctime = time.time()
    if (ctime - last_time) < 0.05:
        return
    cv1 = amyboard.cv_in(channel=0)
    cv2 = amyboard.cv_in(channel=1)
    if cv1 > 10 or cv1 < -10:
        cv1 = 0.0
    if cv2 > 10 or cv2 < -10:
        cv2 = 0.0
	
    history.append((int(10 * cv1),int(10 * cv2)))
    history.remove(history[0])
    update_display()
    
#    UPDATE_INTERVAL = 0.2
#    last_time = ctime
#    ctime = time.time()
#    if (ctime - last_time) > UPDATE_INTERVAL:
