#!/usr/bin/python3
import re


def get_nand2_1_area():
    file_path = "/home/opentools/OpenLane/pdks/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ff_100C_1v65.lib"

    with open(file_path, "r") as f:
        text = f.read()

    # find all cell names that contain "nand2_1"
    cell_names = re.findall(r'cell\s*\(\s*"(sky130_fd_sc_hd__nand2_1\w*)"\s*\)', text)

    for name in cell_names:
        # find where this specific cell's block starts
        start = text.find(f'cell ("{name}")')
        # search for "area :" after that point, before the next cell starts
        end = text.find('cell (', start + 1)
        if end == -1:
            end = len(text)
        cell_text = text[start:end]

        area_match = re.search(r'area\s*:\s*([\d.]+)\s*;', cell_text)
        if area_match:
            print(f"{name} -> area = {area_match.group(1)}")
            return float(area_match.group(1))
        else:
            print(f"{name} -> area not found")
            return None


