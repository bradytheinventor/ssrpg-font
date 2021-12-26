### What is this?
The ASCII-animated game Stone Story RPG has a cool font. But it's saved as a pixel grid, so it can't be used in text editors or other text-based programs.

These scripts process images of the SSRPG font to generate a `.ttf` which can be used in text editors like Word, Notepad, etc.

### How do they work?
1. FFmpeg uses the `cropdetect` and `crop` filters to remove black space from around the image. Saves time manually cropping glyph images.
2. FFmpeg pads the cropped image back to 22x40, in case `cropdetect` was too aggressive.
3. FFmpeg saves the cropped image as a `.bmp` so autotrace can accept it.
4. autotrace detects the glyph. Filtering is turned off to prevent smoothing.
5. autotrace saves the glyph as an `.svg` so FontForge can accept it.
6. FontForge runs in scripting mode with `fontforge_generate_ssrpg.py` as the input.
7. FontForge creates a glyph for each image, imports the `.svg` and `.bmp` for reference, then processes the `.svg` into a font glyph.
8. FontForge saves its work to the `ssrpg.sfd` project.
9. You open the `ssrpg.sfd` project in the desktop version of FontForge for manual post-processing.
10. You generate the font from the GUI.

### How do I generate a font?
Not recommended, I made these scripts for personal use. They're uploaded here mostly for your reference. But if you want to try it yourself, here's what to do:
1. Clone this repository to a Linux computer.
2. Install prerequisites: `sudo apt install ffmpeg`, `sudo apt install fontforge`, `sudo apt install autotrace`
3. Run `trace.sh`. The scripts will generate the FontForge project file `ssrpg.sfd`, which contains the generated glyphs and their reference images.
4. Open `ssrpg.sfd` in the desktop version of FontForge for manual post-processing. Some of the complicated glyphs will have intersecting lines, for example.
5. Use `File>Generate Fonts` to create your `.ttf`. If anything is still wrong with your glyphs, FontForge will tell you so you can go back and fix them.
