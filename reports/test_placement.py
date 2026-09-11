#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

# ---- allow importing nand_area.py from this script's own directory ----
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from nand_area import get_nand2_1_area

reports_dir = sys.argv[1] + "/placement"

file_path1  = reports_dir + "/7-gpl_sta.clock_skew.rpt"
file_path2  = reports_dir + "/7-gpl_sta.max.rpt"
file_path3  = reports_dir + "/7-gpl_sta.min.rpt"
file_path4  = reports_dir + "/7-gpl_sta.rpt"
file_path5  = reports_dir + "/7-gpl_sta.tns.rpt"
file_path6  = reports_dir + "/7-gpl_sta.wns.rpt"
file_path7  = reports_dir + "/8-pl_rsz_sta.area.rpt"
file_path8  = reports_dir + "/8-pl_rsz_sta.clock_skew.rpt"
file_path9  = reports_dir + "/8-pl_rsz_sta.max.rpt"
file_path10 = reports_dir + "/8-pl_rsz_sta.min.rpt"
file_path11 = reports_dir + "/8-pl_rsz_sta.power.rpt"
file_path12 = reports_dir + "/8-pl_rsz_sta.rpt"
file_path13 = reports_dir + "/8-pl_rsz_sta.slew.rpt"
file_path14 = reports_dir + "/8-pl_rsz_sta.tns.rpt"
file_path15 = reports_dir + "/8-pl_rsz_sta.wns.rpt"
file_path16 = reports_dir + "/8-pl_rsz_sta.worst_slack.rpt"

summary_path = os.path.join(reports_dir, "placement_summary.rpt")

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


# ---- Global Clock Skew (before optimization) ----
text_content1 = read_file(file_path1)
if text_content1 is not None:
    pattern1 = re.compile(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+(-?\d+\.\d+)\s*$', re.MULTILINE)
    result1 = pattern1.search(text_content1)
    summary_data["global_skew"] = result1.group(1) if result1 else "N/A"
else:
    summary_data["global_skew"] = "File not found"

# ---- Setup violation (before) ----
text_content2 = read_file(file_path2)
if text_content2 is not None:
    result2 = re.search(r'violated', text_content2, re.IGNORECASE)
    summary_data["setup_violation"] = "Violated" if result2 else "No Violation"
else:
    summary_data["setup_violation"] = "File not found"

# ---- Hold violation (before) ----
text_content3 = read_file(file_path3)
if text_content3 is not None:
    result3 = re.search(r'violated', text_content3, re.IGNORECASE)
    summary_data["hold_violation"] = "Violated" if result3 else "No Violation"
else:
    summary_data["hold_violation"] = "File not found"

# ---- STA unconstrained/global violation (before) ----
text_content4 = read_file(file_path4)
if text_content4 is not None:
    result4 = re.search(r'violated', text_content4, re.IGNORECASE)
    summary_data["sta_violation"] = "Violated" if result4 else "No Violation"
else:
    summary_data["sta_violation"] = "File not found"

# ---- TNS (before) ----
text_content5 = read_file(file_path5)
if text_content5 is not None:
    result5 = re.search(r'tns\s+(-?[\d.]+)', text_content5, re.IGNORECASE)
    summary_data["tns"] = result5.group(1) if result5 else "Not found"
else:
    summary_data["tns"] = "File not found"

# ---- WNS (before) ----
text_content6 = read_file(file_path6)
if text_content6 is not None:
    result6 = re.search(r'wns\s+(-?[\d.]+)', text_content6, re.IGNORECASE)
    summary_data["wns"] = result6.group(1) if result6 else "Not found"
else:
    summary_data["wns"] = "File not found"

# ---- Area + utilization (after optimization) ----
text_content7 = read_file(file_path7)
if text_content7 is not None:
    result7 = re.search(r'Design area\s+([\d.]+)\s*u\^2\s+([\d.]+)%\s*utilization', text_content7, re.IGNORECASE)
    if result7:
        summary_data["area_after_opt_um2"] = result7.group(1)
        summary_data["utilization_after_opt_pct"] = result7.group(2)
    else:
        summary_data["area_after_opt_um2"] = "Not found"
        summary_data["utilization_after_opt_pct"] = "Not found"
else:
    summary_data["area_after_opt_um2"] = "File not found"
    summary_data["utilization_after_opt_pct"] = "File not found"

# ---- Global Clock Skew (after optimization) ----
text_content8 = read_file(file_path8)
if text_content8 is not None:
    pattern8 = re.compile(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+(-?\d+\.\d+)\s*$', re.MULTILINE)
    result8 = pattern8.search(text_content8)
    summary_data["global_skew_after_opt"] = result8.group(1) if result8 else "N/A"
else:
    summary_data["global_skew_after_opt"] = "File not found"

# ---- Setup violation (after optimization) ----
text_content9 = read_file(file_path9)
if text_content9 is not None:
    result9 = re.search(r'violated', text_content9, re.IGNORECASE)
    summary_data["setup_violation_after_opt"] = "Violated" if result9 else "No Violation"
else:
    summary_data["setup_violation_after_opt"] = "File not found"

# ---- Hold violation (after optimization) ----
text_content10 = read_file(file_path10)
if text_content10 is not None:
    result10 = re.search(r'violated', text_content10, re.IGNORECASE)
    summary_data["hold_violation_after_opt"] = "Violated" if result10 else "No Violation"
else:
    summary_data["hold_violation_after_opt"] = "File not found"

# ---- Power (after optimization) ----
text_content11 = read_file(file_path11)
if text_content11 is not None:
    result11 = re.search(r'Total\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', text_content11)
    summary_data["power_after_opt"] = result11.group(4) if result11 else "N/A"
else:
    summary_data["power_after_opt"] = "File not found"

# ---- STA unconstrained/global violation (after optimization) ----
text_content12 = read_file(file_path12)
if text_content12 is not None:
    result12 = re.search(r'violated', text_content12, re.IGNORECASE)
    summary_data["sta_violation_after_opt"] = "Violated" if result12 else "No Violation"
else:
    summary_data["sta_violation_after_opt"] = "File not found"

# ---- Slew / Fanout / Cap violation counts (after optimization) ----
text_content13 = read_file(file_path13)
if text_content13 is not None:
    result13 = re.search(
        r'max slew violation count\s+(\d+)\s*'
        r'max fanout violation count\s+(\d+)\s*'
        r'max cap violation count\s+(\d+)',
        text_content13, re.IGNORECASE
    )
    if result13:
        summary_data["max_slew_violation_count"] = result13.group(1)
        summary_data["max_fanout_violation_count"] = result13.group(2)
        summary_data["max_cap_violation_count"] = result13.group(3)
    else:
        summary_data["max_slew_violation_count"] = "Not found"
        summary_data["max_fanout_violation_count"] = "Not found"
        summary_data["max_cap_violation_count"] = "Not found"
else:
    summary_data["max_slew_violation_count"] = "File not found"
    summary_data["max_fanout_violation_count"] = "File not found"
    summary_data["max_cap_violation_count"] = "File not found"

# ---- TNS (after optimization) ----
text_content14 = read_file(file_path14)
if text_content14 is not None:
    result14 = re.search(r'tns\s+(-?[\d.]+)', text_content14, re.IGNORECASE)
    summary_data["tns_after_opt"] = result14.group(1) if result14 else "Not found"
else:
    summary_data["tns_after_opt"] = "File not found"

# ---- WNS (after optimization) ----
text_content15 = read_file(file_path15)
if text_content15 is not None:
    result15 = re.search(r'wns\s+(-?[\d.]+)', text_content15, re.IGNORECASE)
    summary_data["wns_after_opt"] = result15.group(1) if result15 else "Not found"
else:
    summary_data["wns_after_opt"] = "File not found"

# ---- Worst slack setup & hold (after optimization) ----
text_content16 = read_file(file_path16)
if text_content16 is not None:
    results16 = re.findall(r'worst slack\s+([\d.eE+-]+)', text_content16)
    summary_data["worst_setup_slack_after_opt"] = results16[0] if len(results16) >= 1 else "N/A"
    summary_data["worst_hold_slack_after_opt"] = results16[1] if len(results16) >= 2 else "N/A"
else:
    summary_data["worst_setup_slack_after_opt"] = "File not found"
    summary_data["worst_hold_slack_after_opt"] = "File not found"


# ---- Area in terms of K-NAND2 units (design area / nand2 area) ----
nand2_area = get_nand2_1_area()  # area of sky130_fd_sc_hd__nand2_1 in um^2

try:
    design_area = float(summary_data.get("area_after_opt_um2"))
    if nand2_area:
        summary_data["area_knand2"] = f"{design_area / nand2_area:.2f}"
    else:
        summary_data["area_knand2"] = "NAND2 area not found"
except (TypeError, ValueError):
    # design_area wasn't a valid number (e.g. "Not found" / "File not found")
    summary_data["area_knand2"] = "N/A"


# ============================================================
# Build comparison summary report (before vs after optimization)
# ============================================================
comparison_rows = [
    ("Global Clock Skew",   summary_data.get("global_skew"),        summary_data.get("global_skew_after_opt")),
    ("Setup Violation",     summary_data.get("setup_violation"),     summary_data.get("setup_violation_after_opt")),
    ("Hold Violation",      summary_data.get("hold_violation"),      summary_data.get("hold_violation_after_opt")),
    ("STA Violation",       summary_data.get("sta_violation"),       summary_data.get("sta_violation_after_opt")),
    ("TNS",                 summary_data.get("tns"),                summary_data.get("tns_after_opt")),
    ("WNS",                 summary_data.get("wns"),                summary_data.get("wns_after_opt")),
]

with open(summary_path, "w") as f:
    f.write("=" * 70 + "\n")
    f.write(f"Placement Timing Summary Report - Generated {datetime.now()}\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"{'Metric':<25}{'Before Opt (GPL)':<25}{'After Opt (Resize)':<25}\n")
    f.write("-" * 70 + "\n")
    for metric, before, after in comparison_rows:
        f.write(f"{metric:<25}{str(before):<25}{str(after):<25}\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("Post-Optimization Only Metrics\n")
    f.write("-" * 70 + "\n")
    f.write(f"Design Area (um^2)          : {summary_data.get('area_after_opt_um2')}\n")
    f.write(f"Utilization (%)             : {summary_data.get('utilization_after_opt_pct')}\n")
    f.write(f"Area (K-NAND2 units)        : {summary_data.get('area_knand2')}\n")
    f.write(f"Total Power (leakage, W)    : {summary_data.get('power_after_opt')}\n")
    f.write(f"Worst Setup Slack           : {summary_data.get('worst_setup_slack_after_opt')}\n")
    f.write(f"Worst Hold Slack            : {summary_data.get('worst_hold_slack_after_opt')}\n")
    f.write(f"Max Slew Violations         : {summary_data.get('max_slew_violation_count')}\n")
    f.write(f"Max Fanout Violations       : {summary_data.get('max_fanout_violation_count')}\n")
    f.write(f"Max Cap Violations          : {summary_data.get('max_cap_violation_count')}\n")

print(f"Summary report written to: {summary_path}")