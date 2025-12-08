import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
input_path = BASE_DIR / "backend" / "data" / "sales_data.csv"
output_path = BASE_DIR / "backend" / "data" / "sales_data_render.csv"

MAX_ROWS = 200_000  # adjust if needed

print("Input:", input_path)
print("Output:", output_path)

count = 0

with input_path.open("r", encoding="utf-8", newline="") as fin, \
     output_path.open("w", encoding="utf-8", newline="") as fout:

    reader = csv.reader(fin)
    writer = csv.writer(fout)

    # Write header
    header = next(reader)
    writer.writerow(header)

    for row in reader:
        writer.writerow(row)
        count += 1
        if count >= MAX_ROWS:
            break

print(f"Finished. Wrote {count} rows to {output_path}")
