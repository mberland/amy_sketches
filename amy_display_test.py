import amyboard, random, sequencer, amy

sequencer.tempo(40)

ticks = 0

#amyboard.init_neopixels(num=1, pin=6, seesaw_dev=0x36)
#amyboard.set_neopixel(0, 0, 64, 0, seesaw_dev=0x36)  # dim green
#amyboard.show_neopixels(seesaw_dev=0x36)
rs = random.randint(0,100)
#amyboard.init_neopixels(num=1, pin=6)
err_text = ""

try:
	i2c = amyboard.get_i2c()
except:
    err_text = "no i2c"

def loop():
    global ticks, rs, err_text
    ticks += 1
    if 0 != ticks % 4:
        return
    amyboard.display.fill(0)
    amyboard.display.text(f"{rs}: {random.randint(0,100)}",2,85,255)
    amyboard.display.text(f"err: {err_text}",2,95,255)
    enc_n = amyboard.read_encoder(encoder=0, seesaw_dev=54)
    amyboard.display.text(f"{0}: {enc_n}",2,15,255)
    amyboard.display_refresh()

# Do not edit. Set automatically by the knobs on AMYboard Online.
_auto_generated_knobs = """
i1ic255Z
i1iv6in4Z
i1v0w20F200.000,1.000,,,5.000c2L1G4A,,1000,0.200,100,0.000B0,1.000,1000,0.200,1000,0.000Z
i1v1w4a,,0.000f4.000,0.000,,,,,0.000A,,10000,Z
i1v2w1a,,0.000,0.000c3L1Z
i1v3w2a,,0.000,0.000f220.000L1Z
i1V1.000x0.000,0.000,0.000M0.000,500.000,,0.000,0.000k0.000,320.000,0.500,0.500h0.000,0.850,0.500,3000.000Z
"""
