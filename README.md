# pystickynote

Stickynotes for your desktop easily from the command line! Built using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a modern, lightweight UI.

[Join Discord/Support Discord](https://discord.gg/C7jgQeN)

# Preview

<p align="center">
  <a><img src="https://github.com/M4cs/pystickynote/blob/master/preview.png?raw=true"></a>
</p>

# How does it work?

Pystickynote creates a small window for you to jot your ideas down and then display them later on, all with a command line tool. Notes stay on top of other windows and can be customized with different colors, transparency, and fonts.

# Installation

```bash
git clone https://github.com/rluethy/pystickynote.git
cd pystickynote
pip install .
```

# Running It

```
<pystickynote/pysn> create <name_of_note> # Displays stickynote window

<pystickynote/pysn> open <name_of_note> # Displays old stickynote

<pystickynote/pysn> delete <name_of_note> # Deletes stickynote

<pystickynote/pysn> list # Displays all notes
```

# Changelog

### Update 2.0.0:

- **Migrated from PySimpleGUIQt to CustomTkinter** - Much lighter dependency (~1MB vs ~150MB), no Qt required
- Modern UI with rounded buttons and cleaner styling
- Window now uses system theme colors (matching title bar)
- Text area still respects `background_color` and `text_color` from config
- Requires Python 3.7+ (dropped Python 3.6 support)

### Update 1.5.1:

- Added box_height and box_width values to config

### Update 1.5:

- Added new entry point: `pysn`

- Added delete function thanks to @synackray

- Fixed error with mouse_offset (possibly still buggy)

- New local version of PySimpleGUIQt for that ^

# Configuration

Config files and notes can be found in `~/.config/pystickynote/`. Inside this folder you will find `pysn.conf` and `notes.json`.

You can also find the default config and notes file in this repository.

The config file looks something like this:

```
[DEFAULT]
background_color = #f5f545
text_color = #0a0a0a
alpha = 0.8
border_width = 0
title_size = 24
font_size = 24
box_height = 15
box_width = 80
no_titlebar = False
```

`background_color` = the background hex color for the text area

`text_color` = the text color for the text area

`alpha` = the note window's transparency (0.0 to 1.0)

`border_width` = border around input box and buttons

`font_size` = font size for text

`title_size` = font size for title

`box_height` = height of box

`box_width` = width of box


