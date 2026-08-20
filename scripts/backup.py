"""Create a timestamped SQLite backup. Schedule this with Windows Task Scheduler."""
from datetime import datetime
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
source = root / 'data' / 'tanishi.db'
destination = root / 'backups' / f"tanishi-{datetime.now():%Y%m%d-%H%M%S}.db"
if not source.exists():
    raise SystemExit('No database exists yet.')
destination.parent.mkdir(exist_ok=True)
shutil.copy2(source, destination)
print(destination)
