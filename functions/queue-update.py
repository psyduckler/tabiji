#!/usr/bin/env python3
"""Generic queue JSON status updater.

Usage: python3 queue-update.py <file> <key>=<value> <new_status> [--timestamp]

Handles both flat arrays and nested {"queue": [...]} formats.
Atomic write: writes to temp file then renames.

Examples:
  python3 queue-update.py queue.json slug=new-york done --timestamp
  python3 queue-update.py queue.json id=paris-bracelet in-progress
  python3 queue-update.py queue.json city=Tokyo done
"""
import json, sys, datetime, os, tempfile

def main():
    if len(sys.argv) < 4:
        print("Usage: queue-update.py <file> <key>=<value> <status> [--timestamp]")
        sys.exit(1)

    fpath = sys.argv[1]
    key_val = sys.argv[2]
    new_status = sys.argv[3]
    add_ts = '--timestamp' in sys.argv

    key, val = key_val.split('=', 1)

    with open(fpath) as f:
        data = json.load(f)

    # Handle both {"queue": [...]} and flat [...]
    if isinstance(data, dict) and 'queue' in data:
        items = data['queue']
    else:
        items = data

    found = False
    for item in items:
        if str(item.get(key, '')) == val:
            item['status'] = new_status
            if add_ts:
                ts_key = 'claimedAt' if new_status == 'in-progress' else f"{new_status}At"
                item[ts_key] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            found = True
            break

    if not found:
        print(f"ERROR: {key}={val} not found in {fpath}")
        sys.exit(1)

    # Atomic write via temp file
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(fpath), suffix='.json')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, fpath)
    except Exception:
        os.unlink(tmp)
        raise

    print(f"OK: {key}={val} -> {new_status}")

if __name__ == '__main__':
    main()
