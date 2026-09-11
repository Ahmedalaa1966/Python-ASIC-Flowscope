#!/usr/bin/python3
import os
import subprocess
import sys

LOG_SCRIPTS_DIR = "/home/icpedia/ahmed_alaa/python/log"
RUN_LOGS_PATH = sys.argv[1]

scripts = [
    "syn_log_parsing.py",
    "floorplan_log_parasing.py",
    "placement_log_parasing.py",
    "cts_log_parasing.py",
    "routing_log_parasing.py",
    "signoff_log_parasing.py",
]

for script_name in scripts:
    script_path = os.path.join(LOG_SCRIPTS_DIR, script_name)
    print("=" * 70)
    print(f"Running: {script_name}")
    print("=" * 70)
    if not os.path.exists(script_path):
        print(f"ERROR: Script not found: {script_path}\n")
        continue
    result = subprocess.run(
        [sys.executable, script_path, RUN_LOGS_PATH],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"[stderr from {script_name}]")
        print(result.stderr)
    if result.returncode != 0:
        print(f"WARNING: {script_name} exited with code {result.returncode}\n")

print("=" * 70)
print("All log parsing scripts finished running.")
print("=" * 70)