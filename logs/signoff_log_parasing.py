#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

logs_dir = sys.argv[1] + "/synthesis"

file_path1 = logs_dir + "/1-synthesis.log"

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


text_content1 = read_file(file_path1)

if text_content1 is not None:
    lines = text_content1.splitlines()
    found_error = False
    for line_number, line in enumerate(lines, start=1):
        if re.search(r'error', line, re.IGNORECASE):
            found_error = True
            print(f"[Yosys - Synthesis Stage] [Line {line_number}] {line}")
    if not found_error:
        print("No errors found in synthesis log.")
else:
    print("File not found:", file_path1)