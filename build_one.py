#!/usr/bin/env python3
import subprocess
import sys

# The title from the queue entry (without the pipe character in kathputli)
result = subprocess.run(
    [sys.executable, "scripts/gen_popular_picks_batch.py", "udaipur-kathputli-puppet-workshop||Learn to craft and operate a traditional Rajasthani string puppet in a family artisan workshop in Udaipur.|"],
    cwd="/Users/psy/tabiji",
    capture_output=True,
    text=True
)
print(result.stdout)
print(result.stderr)
