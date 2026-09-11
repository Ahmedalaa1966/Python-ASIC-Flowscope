#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

# ---- allow importing nand_area.py from this script's own directory ----
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from nand_area import get_nand2_1_area

reports_dir = sys.argv[1] + "/synthesis"

file_path1 = reports_dir + "/2-syn_sta.area.rpt"
file_path2 = reports_dir + "/2-syn_sta.wns.rpt"
file_path3 = reports_dir + "/2-syn_sta.power.rpt"
file_path4 = reports_dir + "/2-syn_sta.max.rpt"
file_path5 = reports_dir + "/2-syn_sta.min.rpt"
file_path6 = reports_dir + "/2-syn_sta.slew.rpt"
file_path7 = reports_dir + "/2-syn_sta.tns.rpt"
file_path8 = reports_dir + "/2-syn_sta.worst_slack.rpt"

reports_dir = os.path.dirname(file_path1)
summary_path = os.path.join(reports_dir, "synthesis_summary.rpt")

# a dictionary to store parsed results cleanly, keyed by metric name
summary_data = {}


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


# ---- Area ----
text_content = read_file(file_path1)
if text_content is not None:
    pattern = re.compile(r'(Design area\s)(\d+)')
    result = pattern.search(text_content)
    summary_data["area"] = result.group(2) if result else "N/A"
else:
    summary_data["area"] = "File not found"

# ---- WNS ----
text_content2 = read_file(file_path2)
if text_content2 is not None:
    pattern2 = re.compile(r'(wns\s+)(-?\d+\.?\d*)', re.IGNORECASE)
    result2 = pattern2.search(text_content2)
    summary_data["wns"] = result2.group(2) if result2 else "N/A"
else:
    summary_data["wns"] = "File not found"

# ---- Power ----
text_content3 = read_file(file_path3)
if text_content3 is not None:
    pattern3 = re.compile(r'Total\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)')
    result3 = pattern3.search(text_content3)
    summary_data["power"] = result3.group(4) if result3 else "N/A"
else:
    summary_data["power"] = "File not found"

# ---- Setup violations ----
text_content4 = read_file(file_path4)
if text_content4 is not None:
    pattern4 = re.compile(r'violat\S+')
    result4 = pattern4.search(text_content4)
    summary_data["setup_violation"] = "Yes" if result4 else "No"
else:
    summary_data["setup_violation"] = "File not found"

# ---- Hold violations ----
text_content5 = read_file(file_path5)
if text_content5 is not None:
    pattern5 = re.compile(r'violat\S+')
    result5 = pattern5.search(text_content5)
    summary_data["hold_violation"] = "Yes" if result5 else "No"
else:
    summary_data["hold_violation"] = "File not found"

# ---- Max slew violations ----
text_content6 = read_file(file_path6)
if text_content6 is not None:
    pattern6 = re.compile(r'max slew violation count\s+(\d+)')
    result6 = pattern6.search(text_content6)
    summary_data["slew_violations"] = int(result6.group(1)) if result6 else "N/A"
else:
    summary_data["slew_violations"] = "File not found"

# ---- TNS ----
text_content7 = read_file(file_path7)
if text_content7 is not None:
    pattern7 = re.compile(r'tns\s+([\d.eE+-]+)')
    result7 = pattern7.search(text_content7)
    summary_data["tns"] = result7.group(1) if result7 else "N/A"
else:
    summary_data["tns"] = "File not found"

# ---- Worst slack (setup & hold) ----
text_content8 = read_file(file_path8)
if text_content8 is not None:
    pattern8 = re.compile(r'worst slack\s+([\d.eE+-]+)')
    results8 = pattern8.findall(text_content8)
    if len(results8) >= 2:
        summary_data["worst_setup_slack"] = results8[0]
        summary_data["worst_hold_slack"] = results8[1]
    else:
        summary_data["worst_setup_slack"] = "N/A"
        summary_data["worst_hold_slack"] = "N/A"
else:
    summary_data["worst_setup_slack"] = "File not found"
    summary_data["worst_hold_slack"] = "File not found"


# ---- Area in terms of K-NAND2 units (design area / nand2 area) ----
nand2_area = get_nand2_1_area()  # area of sky130_fd_sc_hd__nand2_1 in um^2

try:
    design_area = float(summary_data.get("area"))
    if nand2_area:
        summary_data["area_knand2"] = f"{design_area / nand2_area:.2f}"
    else:
        summary_data["area_knand2"] = "NAND2 area not found"
except (TypeError, ValueError):
    # design_area wasn't a valid number (e.g. "N/A" / "File not found")
    summary_data["area_knand2"] = "N/A"


# ---- Build a professional report layout ----
line = "=" * 70
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

report = []
report.append(line)
report.append("SYNTHESIS QoR SUMMARY REPORT".center(70))
report.append(line)
report.append(f"Generated on : {timestamp}")
report.append(f"Design       : spm")
report.append(line)
report.append("")

report.append("1. AREA")
report.append("-" * 70)
report.append(f"  Design Area                : {summary_data['area']} um^2")
report.append(f"  Area (K-NAND2 units)       : {summary_data['area_knand2']}")
report.append("")

report.append("2. TIMING")
report.append("-" * 70)
report.append(f"  Worst Negative Slack (WNS) : {summary_data['wns']} ns")
report.append(f"  Total Negative Slack (TNS) : {summary_data['tns']} ns")
report.append(f"  Worst Setup Slack          : {summary_data['worst_setup_slack']} ns")
report.append(f"  Worst Hold Slack           : {summary_data['worst_hold_slack']} ns")
report.append(f"  Setup Violations           : {summary_data['setup_violation']}")
report.append(f"  Hold Violations            : {summary_data['hold_violation']}")
report.append(f"  Max Slew Violations        : {summary_data['slew_violations']}")
report.append("")

report.append("3. POWER")
report.append("-" * 70)
report.append(f"  Total Power                : {summary_data['power']} W")
report.append("")

report.append(line)
report.append("END OF REPORT".center(70))
report.append(line)

summary_text = "\n".join(report) + "\n"


# ---- Write the report ----
summary_fd = os.open(summary_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
os.write(summary_fd, summary_text.encode("utf-8"))
os.close(summary_fd)

print(f"Summary written to {summary_path}")