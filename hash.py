import csv
import json
import os
import sys
from hashlib import sha256


def main():
    if len(sys.argv) != 2:
        print("Usage: python hash.py <csv name>")
        exit()
    
    input_csv = sys.argv[1]

    # Count rows in CSV
    with open(input_csv) as file:
        row_count = sum(1 for _ in file)

    # Get CSV filename
    filename_pair = os.path.splitext(input_csv)
        
    with open(input_csv, "r") as input, open(f"{filename_pair[0]}.output.csv", "w") as output:
        reader = csv.DictReader(input)
        headers = ["Serial Number", "Filename", "UUID", "HASH"]
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()

        for row in reader:
            # Create JSON structure
            dict = {
                "name": row["Filename"],
                "description": "",
                "series_number": row["Serial Number"],
                "series_total": row_count,
                "collection": {
                    "name": "",
                    "id": row["UUID"],
                }
            }

            # Save JSON by filename (if exists in row)
            try:
                if not os.path.exists("./json/"):
                    os.makedirs("./json/")
                if row["Filename"]:
                    with open(f"json/{row['Filename']}.json", "w") as json_output:
                        json.dump(dict, json_output, indent=2)

            except FileNotFoundError:
                sys.exit("File path not found")

            # Hash JSON and add to new CSV
            if row["Filename"]:
                with open(f"json/{row['Filename']}.json", "rb") as json_output:
                    bytes = json_output.read()
                    hash = sha256(bytes).hexdigest()
                    row.update({ "HASH": hash })
                    writer.writerow(row)


if __name__ == "__main__":
    main()