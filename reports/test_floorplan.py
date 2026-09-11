#!/usr/bin/python3
import os
import re
import sys
from datetime import datetime

reports_dir = sys.argv[1] + "/floorplan"
run_dir = sys.argv[1].rsplit("/reports", 1)[0]

file_path1 = reports_dir + "/3-initial_fp_core_area.rpt"
file_path2 = reports_dir + "/3-initial_fp_die_area.rpt"
file_path3 = run_dir + "/logs/floorplan/6-pdn.log"
file_path4 = run_dir + "/logs/floorplan/5-tap.log"



reports_dir = os.path.dirname(file_path1)
summary_path = os.path.join(reports_dir, "floorplan_summary.rpt")

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



# ---- Core Area ----
text_content1 = read_file(file_path1)
if text_content1 is not None:
    numbers = re.findall(r'-?\d+\.?\d*', text_content1)
    if len(numbers) >= 4:
        llx, lly, urx, ury = map(float, numbers[:4])
        summary_data["core_area"] = (urx - llx) * (ury - lly)
        
    else:
        summary_data["core_area"] = "Not found"
else:
    summary_data["core_area"] = "File not found"


# ---- Die Area ----
text_content2 = read_file(file_path2)
if text_content2 is not None:
    numbers = re.findall(r'-?\d+\.?\d*', text_content2)
    if len(numbers) >= 4:
        llx, lly, urx, ury = map(float, numbers[:4])
        summary_data["die_area"] = (urx - llx) * (ury - lly)
    else:
        summary_data["die_area"] = "Not found"
else:
    summary_data["die_area"] = "File not found"

# ---- Core Utilization (core_area / die_area) ----
core_area = summary_data.get("core_area")
die_area = summary_data.get("die_area")
if isinstance(core_area, (int, float)) and isinstance(die_area, (int, float)) and die_area != 0:
    summary_data["core_to_die_utilization_pct"] = (core_area / die_area) * 100
else:
    summary_data["core_to_die_utilization_pct"] = "N/A"

# ---- Power Delivery Network (IR Drop) ----
text_content3 = read_file(file_path3)
if text_content3 is not None:
    # Worstcase voltage
    result_worst_voltage = re.search(r'Worstcase voltage\s*:\s*([\d.eE+-]+)\s*V', text_content3, re.IGNORECASE)
    summary_data["worstcase_voltage"] = result_worst_voltage.group(1) if result_worst_voltage else "Not found"

    # Average IR drop
    result_avg_ir = re.search(r'Average IR drop\s*:\s*([\d.eE+-]+)\s*V', text_content3, re.IGNORECASE)
    summary_data["average_ir_drop"] = result_avg_ir.group(1) if result_avg_ir else "Not found"

    # Worstcase IR drop
    result_worst_ir = re.search(r'Worstcase IR drop\s*:\s*([\d.eE+-]+)\s*V', text_content3, re.IGNORECASE)
    summary_data["worstcase_ir_drop"] = result_worst_ir.group(1) if result_worst_ir else "Not found"
else:
    summary_data["worstcase_voltage"] = "File not found"
    summary_data["average_ir_drop"] = "File not found"
    summary_data["worstcase_ir_drop"] = "File not found"
    
    
# ---- Pins, Endcaps, Tapcells ----
text_content4 = read_file(file_path4)
if text_content4 is not None:
    # Number of pins
    result_pins = re.search(r'Created\s+(\d+)\s+pins', text_content4, re.IGNORECASE)
    summary_data["num_pins"] = result_pins.group(1) if result_pins else "Not found"

    # Number of endcaps
    result_endcaps = re.search(r'Inserted\s+(\d+)\s+endcaps', text_content4, re.IGNORECASE)
    summary_data["num_endcaps"] = result_endcaps.group(1) if result_endcaps else "Not found"

    # Number of tapcells
    result_tapcells = re.search(r'Inserted\s+(\d+)\s+tapcells', text_content4, re.IGNORECASE)
    summary_data["num_tapcells"] = result_tapcells.group(1) if result_tapcells else "Not found"
else:
    summary_data["num_pins"] = "File not found"
    summary_data["num_endcaps"] = "File not found"
    summary_data["num_tapcells"] = "File not found"


# ============================================================
# Build floorplan summary report
# ============================================================
with open(summary_path, "w") as f:
    f.write("=" * 70 + "\n")
    f.write(f"Floorplan Summary Report - Generated {datetime.now()}\n")
    f.write("=" * 70 + "\n\n")

    f.write(f"{'Metric':<30}{'Value':<25}\n")
    f.write("-" * 70 + "\n")
    f.write(f"{'Core Area (um^2)':<30}{str(summary_data.get('core_area')):<25}\n")
    f.write(f"{'Die Area (um^2)':<30}{str(summary_data.get('die_area')):<25}\n")

    ratio = summary_data.get("core_to_die_utilization_pct")
    ratio_str = f"{ratio:.2f}%" if isinstance(ratio, (int, float)) else str(ratio)
    f.write(f"{'Core-to-Die Ratio (%)':<30}{ratio_str:<25}\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("Power Delivery Network (IR Drop)\n")
    f.write("-" * 70 + "\n")
    f.write(f"{'Worstcase Voltage (V)':<30}{str(summary_data.get('worstcase_voltage')):<25}\n")
    f.write(f"{'Average IR Drop (V)':<30}{str(summary_data.get('average_ir_drop')):<25}\n")
    f.write(f"{'Worstcase IR Drop (V)':<30}{str(summary_data.get('worstcase_ir_drop')):<25}\n")

    f.write("\n" + "-" * 70 + "\n")
    f.write("Pins, Endcaps & Tapcells\n")
    f.write("-" * 70 + "\n")
    f.write(f"{'Number of Pins':<30}{str(summary_data.get('num_pins')):<25}\n")
    f.write(f"{'Number of Endcaps':<30}{str(summary_data.get('num_endcaps')):<25}\n")
    f.write(f"{'Number of Tapcells':<30}{str(summary_data.get('num_tapcells')):<25}\n")

print(f"Summary report written to: {summary_path}")