#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

TOOL = "OpenROAD"
STAGE = "Placement"

logs_dir = sys.argv[1] + "/placement"

file_path1 = logs_dir + "/7-global.log"
file_path2 = logs_dir + "/8-resizer.log"
file_path3 = logs_dir + "/9-write_verilog.log"
file_path4 = logs_dir + "/10-detailed.log"
file_paths = [file_path1, file_path2, file_path3, file_path4]

def read_file(path):
    """Read a file using low-level os calls; return decoded text or None."""
    if not os.path.exists(path):
        return None
    fd = os.open(path, os.O_RDONLY)
    stats = os.fstat(fd)
    size = stats.st_size
    raw = os.read(fd, size)
    os.close(fd)
    return raw.decode("utf-8")


def check_log_for_errors(path):
    text_content = read_file(path)
    log_name = os.path.basename(path)

    if text_content is None:
        print(f"[{TOOL} - {STAGE} Stage] File not found: {path}")
        return

    lines = text_content.splitlines()
    found_error = False
    for line_number, line in enumerate(lines, start=1):
        if re.search(r'error', line, re.IGNORECASE):
            found_error = True
            print(f"[{TOOL} - {STAGE} Stage] [{log_name}] [Line {line_number}] {line}")

    if not found_error:
        print(f"[{TOOL} - {STAGE} Stage] [{log_name}] No errors found.")


for path in file_paths:
    check_log_for_errors(path)