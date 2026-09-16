#!/usr/bin/env python3
"""Copy this checkout's runtime files into Omarchy and add its widget, preserving other settings. Re-run after editing Widget.qml/sysmon-stats/manifest.json to sync changes."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--section', choices=['left', 'center', 'right'], default='right')
args = parser.parse_args()
source = Path(__file__).resolve().parent
config_dir = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'omarchy'
config_file = config_dir / 'shell.json'
config = json.loads(config_file.read_text())
layout = config['bar']['layout']
plugin_id = 'io.github.nwohater.sysmon'
runtime_files = ('manifest.json', 'Widget.qml', 'sysmon-stats')
dest = config_dir / 'plugins' / plugin_id
dest.mkdir(parents=True, exist_ok=True)
for name in runtime_files:
    shutil.copy2(source / name, dest / name)
os.chmod(dest / 'sysmon-stats', 0o755)
entry = {'id': plugin_id}
for section in ('left', 'center', 'right'):
    for existing in layout.get(section, []):
        if existing.get('id') == plugin_id:
            entry = existing
    layout[section] = [item for item in layout.get(section, []) if item.get('id') != plugin_id]
layout[args.section].append(entry)
backup = config_file.with_name('shell.json.sysmon-backup-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
shutil.copy2(config_file, backup)
fd, temporary = tempfile.mkstemp(prefix='.shell-sysmon-', dir=config_dir)
try:
    with os.fdopen(fd, 'w') as output:
        output.write(json.dumps(config, indent=2) + '\n')
    os.chmod(temporary, config_file.stat().st_mode & 0o777)
    os.replace(temporary, config_file)
finally:
    Path(temporary).unlink(missing_ok=True)
print(f'Installed System Monitor in the {args.section} section.\nBackup: {backup}\nThe shell should hot-reload the widget.')
