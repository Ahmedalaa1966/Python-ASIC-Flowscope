#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

# ---- allow importing nand_area.py from this script's own directory ----
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from nand_area import get_nand2_1_area

reports_dir = sys.argv[1] + "/signoff"

file_path1  = reports_dir + "/28-rcx_sta.area.rpt"
file_path2  = reports_dir + "/28-rcx_sta.clock_skew.rpt"
file_path3  = reports_dir + "/28-rcx_sta.max.rpt"
file_path4  = reports_dir + "/28-rcx_sta.min.rpt"
file_path5  = reports_dir + "/28-rcx_sta.power.rpt"
file_path6  = reports_dir + "/28-rcx_sta.slew.rpt"
file_path7  = reports_dir + "/28-rcx_sta.tns.rpt"
file_path8  = reports_dir + "/28-rcx_sta.wns.rpt"
file_path9  = reports_dir + "/28-rcx_sta.worst_slack.rpt"
file_path10 = reports_dir + "/29-rcx_mca_sta.area.rpt"
file_path11 = reports_dir + "/29-rcx_mca_sta.clock_skew.rpt"
file_path12 = reports_dir + "/29-rcx_mca_sta.max.rpt"
file_path13 = reports_dir + "/29-rcx_mca_sta.min.rpt"
file_path14 = reports_dir + "/29-rcx_mca_sta.power.rpt"
file_path15 = reports_dir + "/29-rcx_mca_sta.rpt"
file_path16 = reports_dir + "/29-rcx_mca_sta.slew.rpt"
file_path17 = reports_dir + "/29-rcx_mca_sta.tns.rpt"
file_path18 = reports_dir + "/29-rcx_mca_sta.wns.rpt"
file_path19 = reports_dir + "/29-rcx_mca_sta.worst_slack.rpt"
file_path20 = reports_dir + "/32-xor.rpt"
file_path21 = reports_dir + "/drc.rpt"

reports_dir = os.path.dirname(file_path1)
summary_path = os.path.join(reports_dir, "sign_off_summary.rpt")

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


# ---- Area + utilization (after optimization) ----
text_content1 = read_file(file_path1)
if text_content1 is not None:
    result1 = re.search(r'Design area\s+([\d.]+)\s*u\^2\s+([\d.]+)%\s*utilization', text_content1, re.IGNORECASE)
    if result1:
        summary_data["final_area"] = result1.group(1)
        summary_data["final_utilization"] = result1.group(2)
    else:
        summary_data["final_area"] = "Not found"
        summary_data["final_utilization"] = "Not found"
else:
    summary_data["final_area"] = "File not found"
    summary_data["final_utilization"] = "File not found"


# ---- Global Clock Skew (after optimization) ----
text_content2 = read_file(file_path2)
if text_content2 is not None:
    pattern2 = re.compile(r'^\s*-?\d+\.\d+\s+-?\d+\.\d+\s+(-?\d+\.\d+)\s*$', re.MULTILINE)
    result2 = pattern2.search(text_content2)
    summary_data["final_skew"] = result2.group(1) if result2 else "N/A"
else:
    summary_data["final_skew"] = "File not found"

# ---- STA max setup violation (after parasitic extraction) ----
text_content3 = read_file(file_path3)
if text_content3 is not None:
    result3 = re.search(r'violated', text_content3, re.IGNORECASE)
    summary_data["max_setup_violation_after_parasitic_extr"] = "Violated" if result3 else "No Violation"
else:
    summary_data["max_setup_violation_after_parasitic_extr"] = "File not found"

# ---- STA min violation (after optimization) ----
text_content4 = read_file(file_path4)
if text_content4 is not None:
    result4 = re.search(r'violated', text_content4, re.IGNORECASE)
    summary_data["sta_min_violation_after_parasitic_extr"] = "Violated" if result4 else "No Violation"
else:
    summary_data["sta_min_violation_after_parasitic_extr"] = "File not found"

# ---- Power (after parasitic extraction) ----
text_content5 = read_file(file_path5)
if text_content5 is not None:
    result5 = re.search(r'Total\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)', text_content5)
    summary_data["power_after_parasitic_extr"] = result5.group(4) if result5 else "N/A"
else:
    summary_data["power_after_parasitic_extr"] = "File not found"


# ---- STA unconstrained/global violation (after optimization) ----
text_content2 = read_file(file_path2)
if text_content2 is not None:
    result2 = re.search(r'violated', text_content2, re.IGNORECASE)
    summary_data["sta_violation_after_parasitic_extr"] = "Violated" if result2 else "No Violation"
else:
    summary_data["sta_violation_after_parasitic_extr"] = "File not found"

# ---- Slew / Fanout / Cap violation counts (after parasitic extraction) ----
text_content6 = read_file(file_path6)
if text_content6 is not None:
    result6 = re.search(
        r'max slew violation count\s+(\d+)\s*'
        r'max fanout violation count\s+(\d+)\s*'
        r'max cap violation count\s+(\d+)',
        text_content6, re.IGNORECASE
    )
    if result6:
        summary_data["max_slew_violation_count_after_parasitic_extr"] = result6.group(1)
        summary_data["max_fanout_violation_count_after_parasitic_extr"] = result6.group(2)
        summary_data["max_cap_violation_count_after_parasitic_extr"] = result6.group(3)
    else:
        summary_data["max_slew_violation_count_after_parasitic_extr"] = "Not found"
        summary_data["max_fanout_violation_count_after_parasitic_extr"] = "Not found"
        summary_data["max_cap_violation_count_after_parasitic_extr"] = "Not found"
else:
    summary_data["max_slew_violation_count_after_parasitic_extr"] = "File not found"
    summary_data["max_fanout_violation_count_after_parasitic_extr"] = "File not found"
    summary_data["max_cap_violation_count_after_parasitic_extr"] = "File not found"


# ---- TNS (after parasitic extraction) ----
text_content7 = read_file(file_path7)
if text_content7 is not None:
    result7 = re.search(r'tns\s+(-?[\d.]+)', text_content7, re.IGNORECASE)
    summary_data["tns_after_parasitic_extr"] = result7.group(1) if result7 else "Not found"
else:
    summary_data["tns_after_parasitic_extr"] = "File not found"

# ---- WNS (after parasitic extraction) ----
text_content8 = read_file(file_path8)
if text_content8 is not None:
    result8 = re.search(r'wns\s+(-?[\d.]+)', text_content8, re.IGNORECASE)
    summary_data["wns_after_parasitic_extr"] = result8.group(1) if result8 else "Not found"
else:
    summary_data["wns_after_parasitic_extr"] = "File not found"


# ---- Worst slack setup & hold (after parasitic extraction) ----
text_content9 = read_file(file_path9)
if text_content9 is not None:
    results9 = re.findall(r'worst slack\s+([\d.eE+-]+)', text_content9)
    summary_data["worst_setup_slack_after_parasitic_extr"] = results9[0] if len(results9) >= 1 else "N/A"
    summary_data["worst_hold_slack_after_parasitic_extr"] = results9[1] if len(results9) >= 2 else "N/A"
else:
    summary_data["worst_setup_slack_after_parasitic_extr"] = "File not found"
    summary_data["worst_hold_slack_after_parasitic_extr"] = "File not found"


# ---- Clock skew (Slowest / Typical / Fastest corners) (after parasitic extraction) ----
text_content11 = read_file(file_path11)
if text_content11 is not None:
    result_slowest = re.search(
        r'Slowest Corner.*?Skew\s*\n.*?\n\s*[\d.]+\s+[-\d.]+\s+([\d.]+)',
        text_content11, re.DOTALL | re.IGNORECASE
    )
    result_typical = re.search(
        r'Typical Corner.*?Skew\s*\n.*?\n\s*[\d.]+\s+[-\d.]+\s+([\d.]+)',
        text_content11, re.DOTALL | re.IGNORECASE
    )
    result_fastest = re.search(
        r'Fastest Corner.*?Skew\s*\n.*?\n\s*[\d.]+\s+[-\d.]+\s+([\d.]+)',
        text_content11, re.DOTALL | re.IGNORECASE
    )

    summary_data["slowest_corner_skew_after_parasitic_extr"] = result_slowest.group(1) if result_slowest else "Not found"
    summary_data["typical_corner_skew_after_parasitic_extr"] = result_typical.group(1) if result_typical else "Not found"
    summary_data["fastest_corner_skew_after_parasitic_extr"] = result_fastest.group(1) if result_fastest else "Not found"
else:
    summary_data["slowest_corner_skew_after_parasitic_extr"] = "File not found"
    summary_data["typical_corner_skew_after_parasitic_extr"] = "File not found"
    summary_data["fastest_corner_skew_after_parasitic_extr"] = "File not found"


# ---- STA max setup violation (MCA - per corner) ----
text_content12 = read_file(file_path12)
if text_content12 is not None:
    corner_sections12 = re.split(r'(Slowest Corner|Typical Corner|Fastest Corner)', text_content12, flags=re.IGNORECASE)
    corner_status12 = {"Slowest Corner": "N/A", "Typical Corner": "N/A", "Fastest Corner": "N/A"}
    for i in range(1, len(corner_sections12), 2):
        corner_name = corner_sections12[i]
        corner_text = corner_sections12[i + 1] if i + 1 < len(corner_sections12) else ""
        corner_status12[corner_name] = "Violated" if re.search(r'violated', corner_text, re.IGNORECASE) else "No Violation"

    summary_data["setup_violation_slowest"] = corner_status12["Slowest Corner"]
    summary_data["setup_violation_typical"] = corner_status12["Typical Corner"]
    summary_data["setup_violation_fastest"] = corner_status12["Fastest Corner"]
else:
    summary_data["setup_violation_slowest"] = "File not found"
    summary_data["setup_violation_typical"] = "File not found"
    summary_data["setup_violation_fastest"] = "File not found"


# ---- STA min hold violation (MCA - per corner) ----
text_content13 = read_file(file_path13)
if text_content13 is not None:
    corner_sections13 = re.split(r'(Slowest Corner|Typical Corner|Fastest Corner)', text_content13, flags=re.IGNORECASE)
    corner_status13 = {"Slowest Corner": "N/A", "Typical Corner": "N/A", "Fastest Corner": "N/A"}
    for i in range(1, len(corner_sections13), 2):
        corner_name = corner_sections13[i]
        corner_text = corner_sections13[i + 1] if i + 1 < len(corner_sections13) else ""
        corner_status13[corner_name] = "Violated" if re.search(r'violated', corner_text, re.IGNORECASE) else "No Violation"

    summary_data["hold_violation_slowest"] = corner_status13["Slowest Corner"]
    summary_data["hold_violation_typical"] = corner_status13["Typical Corner"]
    summary_data["hold_violation_fastest"] = corner_status13["Fastest Corner"]
else:
    summary_data["hold_violation_slowest"] = "File not found"
    summary_data["hold_violation_typical"] = "File not found"
    summary_data["hold_violation_fastest"] = "File not found"


# ---- Total Power per corner (MCA - after parasitic extraction) ----
text_content14 = read_file(file_path14)
if text_content14 is not None:
    result_slowest_power = re.search(
        r'Slowest Corner.*?Total\s+[\d.eE+-]+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+([\d.eE+-]+)',
        text_content14, re.DOTALL | re.IGNORECASE
    )
    result_typical_power = re.search(
        r'Typical Corner.*?Total\s+[\d.eE+-]+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+([\d.eE+-]+)',
        text_content14, re.DOTALL | re.IGNORECASE
    )
    result_fastest_power = re.search(
        r'Fastest Corner.*?Total\s+[\d.eE+-]+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+([\d.eE+-]+)',
        text_content14, re.DOTALL | re.IGNORECASE
    )

    summary_data["slowest_corner_total_power"] = result_slowest_power.group(1) if result_slowest_power else "Not found"
    summary_data["typical_corner_total_power"] = result_typical_power.group(1) if result_typical_power else "Not found"
    summary_data["fastest_corner_total_power"] = result_fastest_power.group(1) if result_fastest_power else "Not found"
else:
    summary_data["slowest_corner_total_power"] = "File not found"
    summary_data["typical_corner_total_power"] = "File not found"
    summary_data["fastest_corner_total_power"] = "File not found"


# ---- TNS (MCA - after parasitic extraction) ----
text_content17 = read_file(file_path17)
if text_content17 is not None:
    result17 = re.search(r'tns\s+(-?[\d.]+)', text_content17, re.IGNORECASE)
    summary_data["tns_mmc"] = result17.group(1) if result17 else "Not found"
else:
    summary_data["tns_mmc"] = "File not found"

# ---- WNS (MCA - after parasitic extraction) ----
text_content18 = read_file(file_path18)
if text_content18 is not None:
    result18 = re.search(r'wns\s+(-?[\d.]+)', text_content18, re.IGNORECASE)
    summary_data["wns_mmc"] = result18.group(1) if result18 else "Not found"
else:
    summary_data["wns_mmc"] = "File not found"


# ---- Worst slack setup & hold (MCA - after parasitic extraction) ----
text_content19 = read_file(file_path19)
if text_content19 is not None:
    results19 = re.findall(r'worst slack\s+([\d.eE+-]+)', text_content19)
    summary_data["worst_setup_slack_mca"] = results19[0] if len(results19) >= 1 else "N/A"
    summary_data["worst_hold_slack_mca"] = results19[1] if len(results19) >= 2 else "N/A"
else:
    summary_data["worst_setup_slack_mca"] = "File not found"
    summary_data["worst_hold_slack_mca"] = "File not found"


# ---- XOR differences between KLayout and Magic layouts ----
text_content20 = read_file(file_path20)
if text_content20 is not None:
    result20 = re.search(r'Total XOR differences\s*=\s*(\d+)', text_content20, re.IGNORECASE)
    summary_data["xor_diff"] = result20.group(1) if result20 else "Not found"
else:
    summary_data["xor_diff"] = "File not found"


# ---- DRC violation count ----
text_content21 = read_file(file_path21)
if text_content21 is not None:
    result21 = re.search(r'COUNT:\s*(\d+)', text_content21, re.IGNORECASE)
    summary_data["drc_count"] = result21.group(1) if result21 else "Not found"
else:
    summary_data["drc_count"] = "File not found"


# ---- Area in terms of K-NAND2 units (design area / nand2 area) ----
nand2_area = get_nand2_1_area()  # area of sky130_fd_sc_hd__nand2_1 in um^2

try:
    design_area = float(summary_data.get("final_area"))
    if nand2_area:
        summary_data["area_knand2"] = f"{design_area / nand2_area:.2f}"
    else:
        summary_data["area_knand2"] = "NAND2 area not found"
except (TypeError, ValueError):
    # design_area wasn't a valid number (e.g. "Not found" / "File not found")
    summary_data["area_knand2"] = "N/A"


# ============================================================
# Build final summary report
# ============================================================
with open(summary_path, "w") as f:
    f.write("=" * 70 + "\n")
    f.write(f"Signoff Summary Report - Generated {datetime.now()}\n")
    f.write("=" * 70 + "\n\n")

    f.write("-" * 70 + "\n")
    f.write("MCA Corner Details\n")
    f.write("-" * 70 + "\n")
    f.write(f"{'Metric':<25}{'Slowest':<15}{'Typical':<15}{'Fastest':<15}\n")
    f.write(f"{'Setup Violation':<25}{summary_data.get('setup_violation_slowest'):<15}{summary_data.get('setup_violation_typical'):<15}{summary_data.get('setup_violation_fastest'):<15}\n")
    f.write(f"{'Hold Violation':<25}{summary_data.get('hold_violation_slowest'):<15}{summary_data.get('hold_violation_typical'):<15}{summary_data.get('hold_violation_fastest'):<15}\n")
    f.write(f"{'Clock Skew':<25}{summary_data.get('slowest_corner_skew_after_parasitic_extr'):<15}{summary_data.get('typical_corner_skew_after_parasitic_extr'):<15}{summary_data.get('fastest_corner_skew_after_parasitic_extr'):<15}\n")
    f.write(f"{'Total Power':<25}{summary_data.get('slowest_corner_total_power'):<15}{summary_data.get('typical_corner_total_power'):<15}{summary_data.get('fastest_corner_total_power'):<15}\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("Other Signoff Metrics\n")
    f.write("-" * 70 + "\n")
    f.write(f"Design Area (um^2)           : {summary_data.get('final_area')}\n")
    f.write(f"Utilization (%)              : {summary_data.get('final_utilization')}\n")
    f.write(f"Area (K-NAND2 units)         : {summary_data.get('area_knand2')}\n")
    f.write(f"Total Power (rcx_sta, W)     : {summary_data.get('power_after_parasitic_extr')}\n")
    f.write(f"TNS (rcx_sta)                : {summary_data.get('tns_after_parasitic_extr')}\n")
    f.write(f"WNS (rcx_sta)                : {summary_data.get('wns_after_parasitic_extr')}\n")
    f.write(f"TNS (MCA)                    : {summary_data.get('tns_mmc')}\n")
    f.write(f"WNS (MCA)                    : {summary_data.get('wns_mmc')}\n")
    f.write(f"Worst Setup Slack (rcx_sta)  : {summary_data.get('worst_setup_slack_after_parasitic_extr')}\n")
    f.write(f"Worst Hold Slack (rcx_sta)   : {summary_data.get('worst_hold_slack_after_parasitic_extr')}\n")
    f.write(f"Worst Setup Slack (MCA)      : {summary_data.get('worst_setup_slack_mca')}\n")
    f.write(f"Worst Hold Slack (MCA)       : {summary_data.get('worst_hold_slack_mca')}\n")
    f.write(f"Max Slew Violations          : {summary_data.get('max_slew_violation_count_after_parasitic_extr')}\n")
    f.write(f"Max Fanout Violations        : {summary_data.get('max_fanout_violation_count_after_parasitic_extr')}\n")
    f.write(f"Max Cap Violations           : {summary_data.get('max_cap_violation_count_after_parasitic_extr')}\n")
    f.write(f"XOR Differences              : {summary_data.get('xor_diff')}\n")
    f.write(f"DRC Violation Count          : {summary_data.get('drc_count')}\n")

print(f"Summary report written to: {summary_path}")