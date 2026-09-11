#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

# ---- allow importing nand_area.py from this script's own directory ----
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from nand_area import get_nand2_1_area

reports_dir = sys.argv[1] + "/routing"
run_dir = sys.argv[1].rsplit("/reports", 1)[0]

file_path1  = reports_dir + "/15-rt_rsz_sta.area.rpt"
file_path2  = reports_dir + "/15-rt_rsz_sta.clock_skew.rpt"
file_path3  = reports_dir + "/15-rt_rsz_sta.max.rpt"
file_path4  = reports_dir + "/15-rt_rsz_sta.min.rpt"
file_path5  = reports_dir + "/15-rt_rsz_sta.power.rpt"
file_path6  = reports_dir + "/15-rt_rsz_sta.rpt"
file_path7  = reports_dir + "/15-rt_rsz_sta.slew.rpt"
file_path8  = reports_dir + "/15-rt_rsz_sta.tns.rpt"
file_path9  = reports_dir + "/15-rt_rsz_sta.wns.rpt"
file_path10 = reports_dir + "/18-grt_sta.clock_skew.rpt"
file_path11 = reports_dir + "/18-grt_sta.max.rpt"
file_path12 = reports_dir + "/18-grt_sta.min.rpt"
file_path13 = reports_dir + "/18-grt_sta.rpt"
file_path14 = reports_dir + "/18-grt_sta.tns.rpt"
file_path15 = reports_dir + "/18-grt_sta.wns.rpt"
file_path16 = run_dir + "/logs/routing/21-detailed.log"

summary_path = os.path.join(reports_dir, "routing_summary.rpt")

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


# ============================================================
# STEP 15 -> 15-rt_rsz_sta.* (post-resizer repair, comes FIRST)
# ============================================================

# ---- Area + utilization (step 15) ----
text_content1 = read_file(file_path1)
if text_content1 is not None:
    result1 = re.search(r'Design area\s+([\d.]+)\s*u\^2\s+([\d.]+)%\s*utilization', text_content1, re.IGNORECASE)
    if result1:
        summary_data["area_step15"] = result1.group(1)
        summary_data["utilization_step15_pct"] = result1.group(2)
    else:
        summary_data["area_step15"] = "Not found"
        summary_data["utilization_step15_pct"] = "Not found"
else:
    summary_data["area_step15"] = "File not found"
    summary_data["utilization_step15_pct"] = "File not found"

# ---- Global Clock Skew (step 15) ----
text_content2 = read_file(file_path2)
if text_content2 is not None:
    pattern2 = re.compile(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+(-?\d+\.\d+)\s*$', re.MULTILINE)
    result2 = pattern2.search(text_content2)
    summary_data["global_skew_step15"] = result2.group(1) if result2 else "N/A"
else:
    summary_data["global_skew_step15"] = "File not found"

# ---- Setup violation (step 15) ----
text_content3 = read_file(file_path3)
if text_content3 is not None:
    result3 = re.search(r'violated', text_content3, re.IGNORECASE)
    summary_data["setup_violation_step15"] = "Violated" if result3 else "No Violation"
else:
    summary_data["setup_violation_step15"] = "File not found"

# ---- Hold violation (step 15) ----
text_content4 = read_file(file_path4)
if text_content4 is not None:
    result4 = re.search(r'violated', text_content4, re.IGNORECASE)
    summary_data["hold_violation_step15"] = "Violated" if result4 else "No Violation"
else:
    summary_data["hold_violation_step15"] = "File not found"

# ---- Power (step 15) ----
text_content5 = read_file(file_path5)
if text_content5 is not None:
    result5 = re.search(r'Total\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', text_content5)
    summary_data["power_step15"] = result5.group(4) if result5 else "N/A"
else:
    summary_data["power_step15"] = "File not found"

# ---- STA unconstrained/global violation (step 15) ----
text_content6 = read_file(file_path6)
if text_content6 is not None:
    result6 = re.search(r'violated', text_content6, re.IGNORECASE)
    summary_data["sta_violation_step15"] = "Violated" if result6 else "No Violation"
else:
    summary_data["sta_violation_step15"] = "File not found"

# ---- Slew / Fanout / Cap violation counts (step 15) ----
text_content7 = read_file(file_path7)
if text_content7 is not None:
    result7 = re.search(
        r'max slew violation count\s+(\d+)\s*'
        r'max fanout violation count\s+(\d+)\s*'
        r'max cap violation count\s+(\d+)',
        text_content7, re.IGNORECASE
    )
    if result7:
        summary_data["max_slew_violation_count"] = result7.group(1)
        summary_data["max_fanout_violation_count"] = result7.group(2)
        summary_data["max_cap_violation_count"] = result7.group(3)
    else:
        summary_data["max_slew_violation_count"] = "Not found"
        summary_data["max_fanout_violation_count"] = "Not found"
        summary_data["max_cap_violation_count"] = "Not found"
else:
    summary_data["max_slew_violation_count"] = "File not found"
    summary_data["max_fanout_violation_count"] = "File not found"
    summary_data["max_cap_violation_count"] = "File not found"

# ---- TNS (step 15) ----
text_content8 = read_file(file_path8)
if text_content8 is not None:
    result8 = re.search(r'tns\s+(-?[\d.]+)', text_content8, re.IGNORECASE)
    summary_data["tns_step15"] = result8.group(1) if result8 else "Not found"
else:
    summary_data["tns_step15"] = "File not found"

# ---- WNS (step 15) ----
text_content9 = read_file(file_path9)
if text_content9 is not None:
    result9 = re.search(r'wns\s+(-?[\d.]+)', text_content9, re.IGNORECASE)
    summary_data["wns_step15"] = result9.group(1) if result9 else "Not found"
else:
    summary_data["wns_step15"] = "File not found"


# ============================================================
# STEP 18 -> 18-grt_sta.* (global routing STA, comes AFTER step 15)
# ============================================================

# ---- Global Clock Skew (step 18) ----
text_content10 = read_file(file_path10)
if text_content10 is not None:
    pattern10 = re.compile(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+(-?\d+\.\d+)\s*$', re.MULTILINE)
    result10 = pattern10.search(text_content10)
    summary_data["global_skew_step18"] = result10.group(1) if result10 else "N/A"
else:
    summary_data["global_skew_step18"] = "File not found"

# ---- Setup violation (step 18) ----
text_content11 = read_file(file_path11)
if text_content11 is not None:
    result11 = re.search(r'violated', text_content11, re.IGNORECASE)
    summary_data["setup_violation_step18"] = "Violated" if result11 else "No Violation"
else:
    summary_data["setup_violation_step18"] = "File not found"

# ---- Hold violation (step 18) ----
text_content12 = read_file(file_path12)
if text_content12 is not None:
    result12 = re.search(r'violated', text_content12, re.IGNORECASE)
    summary_data["hold_violation_step18"] = "Violated" if result12 else "No Violation"
else:
    summary_data["hold_violation_step18"] = "File not found"

# ---- STA unconstrained/global violation (step 18) ----
text_content13 = read_file(file_path13)
if text_content13 is not None:
    result13 = re.search(r'violated', text_content13, re.IGNORECASE)
    summary_data["sta_violation_step18"] = "Violated" if result13 else "No Violation"
else:
    summary_data["sta_violation_step18"] = "File not found"

# ---- TNS (step 18) ----
text_content14 = read_file(file_path14)
if text_content14 is not None:
    result14 = re.search(r'tns\s+(-?[\d.]+)', text_content14, re.IGNORECASE)
    summary_data["tns_step18"] = result14.group(1) if result14 else "Not found"
else:
    summary_data["tns_step18"] = "File not found"

# ---- WNS (step 18) ----
text_content15 = read_file(file_path15)
if text_content15 is not None:
    result15 = re.search(r'wns\s+(-?[\d.]+)', text_content15, re.IGNORECASE)
    summary_data["wns_step18"] = result15.group(1) if result15 else "Not found"
else:
    summary_data["wns_step18"] = "File not found"


# ---- Detail Routing Summary (file_path16) ----
text_content16 = read_file(file_path16)
if text_content16 is not None:
    # Total wire length
    result_total = re.search(r'Total wire length\s*=\s*([\d.]+)\s*um', text_content16, re.IGNORECASE)
    summary_data["total_wire_length_um"] = result_total.group(1) if result_total else "Not found"

    # Per-layer wire lengths (li1, met1, met2, met3, met4, met5, ...)
    layer_matches = re.findall(r'Total wire length on LAYER\s+(\S+)\s*=\s*([\d.]+)\s*um', text_content16, re.IGNORECASE)
    for layer_name, layer_length in layer_matches:
        summary_data[f"wire_length_{layer_name}_um"] = layer_length

    # Total number of vias
    result_vias = re.search(r'Total number of vias\s*=\s*(\d+)', text_content16, re.IGNORECASE)
    summary_data["total_vias"] = result_vias.group(1) if result_vias else "Not found"
else:
    summary_data["total_wire_length_um"] = "File not found"
    summary_data["total_vias"] = "File not found"


# ---- Area in terms of K-NAND2 units (step 15 area / nand2 area) ----
nand2_area = get_nand2_1_area()  # area of sky130_fd_sc_hd__nand2_1 in um^2

try:
    design_area = float(summary_data.get("area_step15"))
    if nand2_area:
        summary_data["area_knand2"] = f"{design_area / nand2_area:.2f}"
    else:
        summary_data["area_knand2"] = "NAND2 area not found"
except (TypeError, ValueError):
    # design_area wasn't a valid number (e.g. "Not found" / "File not found")
    summary_data["area_knand2"] = "N/A"


# ============================================================
# Overall Status Summary (PASS/FAIL rollup across all checks)
# ============================================================
violation_keys = [
    "setup_violation_step15", "hold_violation_step15", "sta_violation_step15",
    "setup_violation_step18", "hold_violation_step18", "sta_violation_step18",
]
violations_found = [k for k in violation_keys if summary_data.get(k) == "Violated"]

summary_data["overall_status"] = "FAIL" if violations_found else "PASS"
summary_data["violations_list"] = ", ".join(violations_found) if violations_found else "None"


# ============================================================
# Build comparison summary report (step 15 vs step 18)
# ============================================================
comparison_rows = [
    ("Global Clock Skew",   summary_data.get("global_skew_step15"),   summary_data.get("global_skew_step18")),
    ("Setup Violation",     summary_data.get("setup_violation_step15"), summary_data.get("setup_violation_step18")),
    ("Hold Violation",      summary_data.get("hold_violation_step15"),  summary_data.get("hold_violation_step18")),
    ("STA Violation",       summary_data.get("sta_violation_step15"),   summary_data.get("sta_violation_step18")),
    ("TNS",                 summary_data.get("tns_step15"),             summary_data.get("tns_step18")),
    ("WNS",                 summary_data.get("wns_step15"),             summary_data.get("wns_step18")),
]

with open(summary_path, "w") as f:
    f.write("=" * 70 + "\n")
    f.write(f"Routing Timing Summary Report - Generated {datetime.now()}\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"Overall Status: {summary_data.get('overall_status')}\n")
    f.write(f"Violations Found: {summary_data.get('violations_list')}\n\n")

    f.write(f"{'Metric':<25}{'Step 15 (Resize)':<25}{'Step 18 (GRT)':<25}\n")
    f.write("-" * 70 + "\n")
    for metric, step15, step18 in comparison_rows:
        f.write(f"{metric:<25}{str(step15):<25}{str(step18):<25}\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("Step 15 (Resize) Only Metrics\n")
    f.write("-" * 70 + "\n")
    f.write(f"Design Area (um^2)          : {summary_data.get('area_step15')}\n")
    f.write(f"Utilization (%)             : {summary_data.get('utilization_step15_pct')}\n")
    f.write(f"Area (K-NAND2 units)        : {summary_data.get('area_knand2')}\n")
    f.write(f"Total Power (leakage, W)    : {summary_data.get('power_step15')}\n")
    f.write(f"Max Slew Violations         : {summary_data.get('max_slew_violation_count')}\n")
    f.write(f"Max Fanout Violations       : {summary_data.get('max_fanout_violation_count')}\n")
    f.write(f"Max Cap Violations          : {summary_data.get('max_cap_violation_count')}\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("Detail Routing Summary\n")
    f.write("-" * 70 + "\n")
    f.write(f"Total Wire Length (um)      : {summary_data.get('total_wire_length_um')}\n")
    for key, value in summary_data.items():
        if key.startswith("wire_length_") and key.endswith("_um"):
            layer_name = key[len("wire_length_"):-len("_um")]
            f.write(f"  Wire Length on {layer_name:<10} : {value} um\n")
    f.write(f"Total Number of Vias        : {summary_data.get('total_vias')}\n")

print(f"Summary report written to: {summary_path}")