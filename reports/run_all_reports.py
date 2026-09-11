#!/usr/bin/python3
import os
import subprocess
import sys

REPORT_SCRIPTS_DIR = "/home/icpedia/ahmed_alaa/python/reports"
RUN_REPORTS_PATH = sys.argv[1]

scripts = [
    "test_syn.py",
    "test_floorplan.py",
    "test_placement.py",
    "test_cts.py",
    "test_routing.py",
    "test_signoff.py",
]

for script_name in scripts:
    script_path = os.path.join(REPORT_SCRIPTS_DIR, script_name)
    print("=" * 70)
    print(f"Running: {script_name}")
    print("=" * 70)
    if not os.path.exists(script_path):
        print(f"ERROR: Script not found: {script_path}\n")
        continue
    result = subprocess.run(
        [sys.executable, script_path, RUN_REPORTS_PATH],
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
print("All report summary scripts finished running.")
print("=" * 70)