#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

TOOL = "OpenROAD"
STAGE = "Routing"

logs_dir = sys.argv[1] + "/routing"

file_path1 = logs_dir + "/15-resizer.log"
file_path2 = logs_dir + "/16-write_verilog.log"
file_path3 = logs_dir + "/17-diode_legalization.log"
file_path4 = logs_dir + "/18-global.log"
file_path5 = logs_dir + "/19-fill.log"
file_path6 = logs_dir + "/20-write_verilog_global.log"
file_path7 = logs_dir + "/21-detailed.log"
file_path8 = logs_dir + "/22-write_verilog_detailed.log"
file_paths = [file_path1, file_path2, file_path3, file_path4,
              file_path5, file_path6, file_path7, file_path8]

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
    """Return True if at least one error line was printed for this file."""
    text_content = read_file(path)
    log_name = os.path.basename(path)

    if text_content is None:
        print(f"[{TOOL} - {STAGE} Stage] File not found: {path}")
        return False

    lines = text_content.splitlines()
    found_error = False
    for line_number, line in enumerate(lines, start=1):
        if re.search(r'error', line, re.IGNORECASE):
            found_error = True
            print(f"[{TOOL} - {STAGE} Stage] [{log_name}] [Line {line_number}] {line}")

    return found_error


any_error = False
for path in file_paths:
    if check_log_for_errors(path):
        any_error = True

if not any_error:
    print(f"[{TOOL} - {STAGE} Stage] No errors found in any routing log.")