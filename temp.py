import csv

names = []
with open("pc-part-picker-dump/cpu.csv", "r") as f:
    rows = csv.DictReader(f)

    for row in rows:
        names.append(" ".join(row["Name"].strip().lower().split()[:-1]) + "\n")


with open("cpu_names.txt", "w") as f:
    f.writelines(names)
