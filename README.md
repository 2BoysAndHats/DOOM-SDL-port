# DOOM-SDL-port
A functional Windows port of the original DOOM source code

## Introduction
Seeing that the original DOOM source is freely available online, and as I was looking for an excuse to learn more about low-level game development and porting, I decided to try to port DOOM to Windows. This repository contains the result.

This isn't meant to be the best DOOM source port in the world, or even a fully feature complete version. This is meant primarily as an educational resource that might hopefully be of value to those looking to do something similar.

A sidenote: if you *are* looking for a feature-complete version of DOOM, [Chocolate Doom](https://github.com/chocolate-doom/chocolate-doom) is a good place to start. It's cross-platform, has a clean codebase, and is fully compatible with the original DOOM (even going as far as to replicate some of its bugs!)

## Building
If you're looking to build DOOM-SDL-port, you'll need the following:
* Visual Studio 2017
* A copy of a DOOM `.wad` file (the file that contains the level data)
* A soundfont file (to play the music) - I recommend [SGM-V2.01](https://archive.org/details/SGM-V2.01)
* [DOSBox](https://www.dosbox.com/) and [Python](https://python.org) (to convert the music in the WAD file - see Music setup below)

To build, first clone the project source and open it up in Visual Studio. Make sure the build target is set to x86, and build. Hopefully, it'll complete without errors. Unfortunately, it'll probably fail to run, complaining about a bunch of missing libraries. To fix that, copy all of the DLLs in the `linuxdoom-1.1.0/runtime_library` folder into the `linuxdoom-1.1.0/Debug` folder (the same folder as the DOOM-SDL-port.exe executable).

## Music setup
DOOM's music is stored in the MUS format, a somewhat archaic format similar to MIDI. There isn't a lot of documentation available on the format itself, so DOOM-SDL-port requires that any input WAD file have all music lumps converted to MIDI. DOOM-SDL-port achieves this via a small python script that scans through the WAD, finds all of these music lumps, and runs them through the bundled `mus2midi.exe` converter (by just_joe). Given that this written at the same time as the original DOOM, you'll also need a copy of DOSBox for the script to be able to run it.

To start, open up `dosbox.conf` (found in the `music_converter` folder) in a text editor of your choice, scroll all the way to the bottom, and edit the last two lines:
```
MOUNT C <mus2midi directory>
C:
```

Change `<mus2midi directory>` to wherever your copy of the `music_converter` folder is. For example:
```
MOUNT C C:\Users\2BoysAndHats\Projects\DOOM-SDL-PORT\music_converter
C:
```
To actually run the conversion, run `python music_converter.py <path to your WAD file>`, filling in the path of the DOOM WAD file you downloaded earlier. If all goes well, a bunch of DOSBOX windows should start opening and closing as it converts each music lump in turn. When the dust settles, you should have a new WAD file in the `music_converter` folder called `midi-<your wad name>.wad`. Move this converted file into the `linuxdoom-1.10/Debug` folder, and **make sure to rename it back to what is was before** (usually something like doom.wad, or doom1.wad)! DOOM-SDL-port won't recognise your WAD file otherwise.

Finally, take a soundfont of your choosing, and place it also into the `linuxdoom-1.10/Debug` folder, making sure to call it "soundfont.sf2". With this, should be able to start up DOOM (by running DOOM-SDL-port.exe, or just rebuilding the project in Visual Studio), and play to your heart's content!

