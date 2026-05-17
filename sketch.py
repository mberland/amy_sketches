# AMYboard Sketch
# Code put here runs first, then loop() is called every 32nd note.
import amyboard, amy
import random

foo = 0
amyboard.display.fill(0)
amyboard.display.show()
#amyboard.show_midi_ccs(ticks_to_display=60)

def random_note(low=40,high=62,modifier=4):
    x = random.randint(low,high)
    x = modifier * int(x / modifier)
    return x

def cv_to_patch(cvv):
    return int(((10.0+cvv)/20.0)*256)

amy.send(synth=1, patch=10, num_voices=4)

def loop():
    global foo
    cv1 = round(amyboard.cv_in(channel=0),2)
    cv2 = round(amyboard.cv_in(channel=1),2)
    note = int(cv2 + 40) #random_note()
    patch_number = cv_to_patch(cv1)
    amyboard.display.fill(0)
    amyboard.display.text(f"synth: {patch_number}",10,10,255)
    amyboard.display.text(f" note: {note}",10,20,255)
    amyboard.display.text(f"  cv1: {cv1}",10,30,255)
    amyboard.display.text(f"  cv2: {cv2}",10,40,255)
    amyboard.display.refresh()
    foo = foo + 1
    if 0 == foo % (2 * random.randint(1,4)):
        amy.send(synth=1,vel=0)
        amy.send(synth=1,patch=patch_number)
        amy.send(synth=1,vel=1,note=note)
        

# Do not edit. Set automatically by the knobs on AMYboard Online.
_auto_generated_knobs = """
i1ic255Z
i1iv6in4Z
i1v0w20a1.350F1003.665,1.000,,,2.283R1.803c2L1G4A,,644,0.402,137,0.000B39,1.000,827,0.307,679,0.000Z
i1v1w4a,,0.000f2.016,0.000,,,,,0.000A5,,100,1.000,10000,0.000Z
i1v2w2a0.199,,0.000,0.000f441.640d0.627c3L1Z
i1v3w1a0.256,,0.000,0.000f219.946d0.635L1Z
i1V5.906x0.827,3.661,8.386M0.186,198.685,,0.492,0.000k0.561,320.000,0.741,0.501h1.000,0.775,0.735,3000.000Z
i1ic70,1,50.000,2000.000,0.000,i%iv2f%vZ
i1ic71,0,0.000,9.000,0.000,i%iv2w%vZ
i1ic72,0,0.500,0.990,0.000,i%iv2d%vZ
i1ic73,1,0.000,1.000,0.100,i%iv2a%v,,0,0Z
i1ic74,1,20.000,8000.000,0.000,i%iv0F%vZ
i1ic75,1,0.500,16.000,0.000,i%iv0R%vZ
i1ic76,0,0.000,1.000,0.000,i%iv0F,%vZ
i1ic77,0,-10.000,10.000,0.000,i%iv0F,,,,%vZ
i1ic78,0,-15.000,15.000,0.000,x%vZ
i1ic79,0,-15.000,15.000,0.000,x,%vZ
i1ic80,0,-15.000,15.000,0.000,x,,%vZ
i1ic81,1,50.000,2000.000,0.000,i%iv3f%vZ
i1ic82,0,0.000,9.000,0.000,i%iv3w%vZ
i1ic83,0,0.500,0.990,0.000,i%iv3d%vZ
i1ic84,1,0.001,1.000,0.100,i%iv3a%v,,0,0Z
i1ic85,0,0.000,1000.000,0.000,i%iv0B%v,1,,,,0Z
i1ic86,1,0.000,2000.000,50.000,i%iv0B,1,%v,,,0Z
i1ic87,0,0.000,1.000,0.000,i%iv0B,1,,%v,,0Z
i1ic88,1,0.000,8000.000,50.000,i%iv0B,1,,,%v,0Z
i1ic89,1,0.000,1.000,0.100,k%vZ
i1ic90,1,0.100,20.000,0.000,k,,%vZ
i1ic91,0,0.010,1.000,0.000,k,,,%vZ
i1ic92,1,0.100,20.000,0.000,i%iv1f%vZ
i1ic94,1,0.000,4.000,0.001,i%iv2f,,,,,%vZi%iv3f,,,,,%vZ
i1ic95,0,0.000,0.490,0.000,i%iv2d,,,,,%vZi%iv3d,,,,,%vZ
i1ic96,0,0.000,4.000,0.001,i%iv0F,,,,,%vZ
i1ic97,0,0.000,1000.000,0.000,i%iv0A%v,1,,,,0Z
i1ic98,1,0.000,2000.000,50.000,i%iv0A,1,%v,,,0Z
i1ic99,0,0.000,1.000,0.000,i%iv0A,1,,%v,,0Z
i1ic100,1,0.000,8000.000,50.000,i%iv0A,1,,,%v,0Z
i1ic101,1,0.000,1.000,0.100,h%vZ
i1ic102,0,0.000,1.000,0.000,h,%vZ
"""
