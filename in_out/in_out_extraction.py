#!/usr/bin/python3

# Fill in the path to your netlist file
NETLIST_PATH = "/home/opentools/OpenLane/designs/wbqspiflash/runs/RUN_2026.09.06_11.06.39/results/synthesis/wbqspiflash.AREA0.v"
OUTPUT_PATH = "/home/opentools/OpenLane/designs/wbqspiflash/in_out.txt"

with open(NETLIST_PATH, "r") as f:
    lines = f.readlines()

inputs = []
outputs = []

for line in lines:
    line = line.strip()
    if line.startswith("input"):
        inputs.append(line)
    elif line.startswith("output"):
        outputs.append(line)

with open(OUTPUT_PATH, "w") as out:
    out.write("INPUTS:\n")
    for i in inputs:
        out.write(i + "\n")

    out.write("\nOUTPUTS:\n")
    for o in outputs:
        out.write(o + "\n")

print("Saved to in_out.txt")