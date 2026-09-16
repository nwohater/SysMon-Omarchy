# System Monitor (Omarchy bar plugin)

Live total CPU % and memory % usage in the Omarchy status bar.

## Install

```bash
python3 install.py               # adds to the right section
python3 install.py --section left
```

This symlinks this checkout into `~/.config/omarchy/plugins/io.github.nwohater.sysmon`
and appends the widget to `~/.config/omarchy/shell.json`. The shell hot-reloads
on save, so the widget should appear immediately.

## How it works

`sysmon-stats` samples `/proc/stat` over a 0.3s window to compute total CPU
busy %, and reads `/proc/meminfo` for used memory %. `Widget.qml` runs it
every 2 seconds and renders `CPU N%  MEM N%`. Click the widget to open `btop`.

## Uninstall

```bash
omarchy plugin remove io.github.nwohater.sysmon
```
