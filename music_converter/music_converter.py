"""
music_converter.py

Takes in a DOOM WAD file, and converts all the music from DOOM's MUS format to MIDI
using mus2midi.exe and dosbox

by 2BoysAndHats
"""

import sys
import os
import struct
import subprocess

############
# Settings #
############

# Path to DOSBOX. Used to emulate mus2mid
DOSBOX_PATH = "C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe"

# Path to DOSBOX config. Used so DOSBOX knows where mus2midi is located
CONFIG_PATH = "dosbox.conf"

def convert_wad(filepath):
    lumps = []

    with open(filepath, 'rb') as f:
        wad = f.read()

    number_lumps = struct.unpack('<I', wad[4:8])[0]
    directory_start = struct.unpack('<I', wad[8:12])[0]

    for i in range(number_lumps):
        lump_directory_start = i * 16 + directory_start # each entry is 16 bytes

        lump_start = struct.unpack('<I', wad[lump_directory_start: lump_directory_start + 4])[0] # pointer to the actual lump data
        lump_size = struct.unpack('<I', wad[lump_directory_start + 4: lump_directory_start + 8])[0] # length of the lump, in bytes
        lump_name = wad[lump_directory_start + 8: lump_directory_start + 16].decode('utf-8').replace('\x00', '')

        lump_data = wad[lump_start: lump_start + lump_size]

        if lump_data[0:4] == "MUS\x1a".encode("utf8"):
            print (f"Converting music lump {lump_name}")
            
            # write it to a file so DOSBOX can see it
            with open(f"{lump_name}.mus", "wb") as f:
                f.write(lump_data)

            dosbox_process = subprocess.Popen([
                DOSBOX_PATH,
                "-exit",
                "-c",
                f"mus2midi.exe {lump_name}.mus {lump_name}.mid",
                "mus2midi.exe" # a bit hacky, but dosbox needs an executable to run so it can exit properly
            ])

            dosbox_process.wait()

            # and read it back in
            with open(f"{lump_name}.mid", "rb") as f:
                midi_data = f.read()

            # delete the temporary files
            os.remove(f"{lump_name}.mus")
            os.remove(f"{lump_name}.mid")

            lumps.append((lump_name, midi_data))
        else:
            # save it verbatim
            lumps.append((lump_name, lump_data))

    # Now that we've read and processed everything, let's reassemble the WAD file
    with open("midi-" + filepath, "wb") as f:
        f.write("IWAD".encode("utf8")) # WAD file header
        f.write(struct.pack('<I', number_lumps)) # How many lumps we have

        total_lump_length = sum([len(i[1]) for i in lumps])
        f.write(struct.pack('<I', total_lump_length + 12)) # directory start

        # now write all of our lumps
        for (name, lump) in lumps:
            f.write(lump)
        
        # and the directory
        address_cum_sum = 12 # Cumulative sums to represent the lump starting addresses
        for (name, lump) in lumps:
            f.write(struct.pack('<I', address_cum_sum)) # starting address
            f.write(struct.pack('<I', len(lump))) # lump length
            f.write((name + '\x00' * (8 - len(name))).encode('utf8')) # lump name, padded with null bytes
            address_cum_sum += len(lump)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Please specify a WAD file to convert")
        sys.exit(1)

    convert_wad(sys.argv[1])