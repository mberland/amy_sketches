def create_pd_patch(filename="generated_synth.pd"):
    # Pure Data patch syntax template
    # Format: #X obj [X-pos] [Y-pos] [object_name] [arguments];
    # Format: #X connect [source_obj_id] [outlet_index] [target_obj_id] [inlet_index];
    
    pd_lines = [
        "#N canvas 200 200 450 300 12;",                    # Create a canvas window (X, Y, width, height, font_size)
        "#X obj 50 40 line;",                                # Object 0: [line] for smooth parameter changes
        "#X obj 50 80 osc~ 440;",                            # Object 1: [osc~] at 440Hz base frequency
        "#X obj 180 80 floatatom 0 0 0 0 - - - 0;",          # Object 2: GUI Number atom for volume (0.0 to 1.0)
        "#X obj 50 130 *~ 0.1;",                             # Object 3: [*~] multiplier for audio volume control
        "#X obj 50 180 dac~;",                               # Object 4: [dac~] digital-to-analog converter (Output)
        "#X msg 50 10 220 500;",                             # Object 5: Message box [220 500( to glide frequency
        
        # Object Connections (IDs are 0-indexed in order of creation above)
        "#X connect 0 0 1 0;",                               # Connect [line] out -> [osc~] frequency inlet
        # Connect [osc~] out -> [*~] left inlet
        "#X connect 1 0 3 0;",                               
        # Connect volume number box -> [*~] right inlet
        "#X connect 2 0 3 1;",                               
        # Connect [*~] out -> [dac~] left channel
        "#X connect 3 0 4 0;",                               
        # Connect [*~] out -> [dac~] right channel
        "#X connect 3 0 4 1;",                               
        # Connect glide message -> [line] input
        "#X connect 5 0 0 0;"                                
    ]
    
    # Joint lines with newlines and save the file
    patch_content = "\n".join(pd_lines)
    
    with open(filename, "w") as f:
        f.write(patch_content)
        
    print(f"Success! Pure Data patch saved as '{filename}'")

if __name__ == "__main__":
    create_pd_patch()
