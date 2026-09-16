# System Monitor (Omarchy bar plugin)

Live total CPU % and memory % usage in the Omarchy status bar.

## Install

```bash
omarchy plugin add https://github.com/nwohater/SysMon-Omarchy.git --enable
```

This clones the plugin as a git checkout into
`~/.config/omarchy/plugins/io.github.nwohater.sysmon` and adds the widget to
the bar (defaults to the right section).

To place it in a specific section instead of accepting the prompt:

```bash
omarchy plugin add https://github.com/nwohater/SysMon-Omarchy.git
omarchy plugin enable io.github.nwohater.sysmon --section left
```

## Update

Because it's installed as a git checkout, pulling in new commits from this
repo is a single command:

```bash
omarchy plugin update io.github.nwohater.sysmon
```

This fast-forwards from `origin`, re-validates the plugin, and rolls back
automatically if validation fails — so a bad update can't break your bar.

## How it works

`sysmon-stats` samples `/proc/stat` over a 0.3s window to compute total CPU
busy %, and reads `/proc/meminfo` for used memory %. `Widget.qml` runs it
every 2 seconds and renders `CPU N%  MEM N%`, highlighting when either value
hits 80%+. Click the widget to open `btop`.

## Uninstall

```bash
omarchy plugin remove io.github.nwohater.sysmon
```
