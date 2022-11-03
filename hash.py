import csv
import json
import os
import sys
from hashlib import sha256


def main():
    if len(sys.argv) != 2:
        print("Usage: python hash.py <csv name>")
        exit()
    
    input_file = sys.argv[1]

    # Count rows in CSV
    with open(input_file) as file:
        row_count = sum(1 for row in file)

    # Get CSV filename
    filename_pair = os.path.splitext(input_file)
        
    with open(input_file, "r") as input_csv, open(f"{filename_pair[0]}.output.csv", "w") as output_csv:
        reader = csv.DictReader(input_csv)
        headers = ["Serial Number", "Filename", "UUID", "HASH"]
        writer = csv.DictWriter(output_csv, fieldnames=headers)
        writer.writeheader()

        for row in reader:
            # Write JSON
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

            # Create JSONs by filenames
            try:
                if not os.path.exists("./json/"):
                    os.makedirs("./json/")
                with open(f"json/{row['Filename']}.json", "w") as json_output:
                    json.dump(dict, json_output, indent=2)
            except FileNotFoundError:
                sys.exit("File path not found")

            # Hash JSON and add to new CSV
            with open(f"json/{row['Filename']}.json", "rb") as json_output:
                bytes = json_output.read()
                hash = sha256(bytes).hexdigest()

                # Update row with hash
                row.update({ "HASH": hash })
                writer.writerow(row)


if __name__ == "__main__":
    main()