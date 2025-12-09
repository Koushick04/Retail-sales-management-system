# tools/create_render_csv.py
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "backend" / "data" / "sales_data.csv"
OUTPUT = BASE / "backend" / "data" / "sales_data_render.csv"

MAX_ROWS = 80_000  # change if you want a different count

def create_sample():
    if not INPUT.exists():
        print("Input not found:", INPUT)
        return
    count = 0
    with INPUT.open("r", encoding="utf-8", newline="") as fin, \
         OUTPUT.open("w", encoding="utf-8", newline="") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)
            count += 1
            if count >= MAX_ROWS:
                break
    print(f"Wrote {count} rows to {OUTPUT}")

if __name__ == "__main__":
    create_sample()
