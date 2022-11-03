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
        total_rows = sum(1 for _ in file) - 1

    # Get CSV filename
    filename_pair = os.path.splitext(input_csv)
        
    with open(input_csv, "r") as input, open(f"{filename_pair[0]}.output.csv", "w") as output:
        reader = csv.DictReader(input)
        headers = ["TEAM NAMES", "Series Number", "Filename", "Name", "Description", "Gender", "Attributes", "UUID", "Hash"]
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()

        row_count = 1
        bad_rows = 0

        for row in reader:
            # Create JSON structure
            dict = {
                "format": "CHIP-0007",
                "name": row["Filename"],
                "description": row["Description"],
                "minting_tool": "TEAM NAMES",
                "sensitive_content": False,
                "series_number": row["Series Number"],
                "series_total": total_rows,
                "attributes": [],
                "collection": {
                    "name": "Zuri NFT Tickets for Free Lunch",
                    "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
                    "attributes": [
                        {
                            "type": "description",
                            "value": "Rewards for accomplishments during HNGi9."
                        }
                    ]
                }
            }

            # Add attributes to JSON
            try:
                dict.update(parse_attributes(row["Attributes"]))
            except Exception:
                bad_rows += 1
                continue
            else:
                row_count += 1

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
                    row.update({ "Hash": hash })
                    writer.writerow(row)

    print(f"{row_count} JSONs created")
    print(f"{bad_rows} bad rows")

def parse_attributes(attributes):
    attributes = attributes.strip().split(";")

    # List of attribute values in order
    row = []

    for attribute in attributes:
        attribute_value = attribute.split(":")
        row.append(attribute_value[1].strip())
    
    attribute_dict = {
        "hair": row[0],
        "eyes": row[1],
        "teeth": row[2],
        "clothing": row[3],
        "accessories": row[4],
        "expression": row[5],
        "strength": row[6],
        "weakness": row[7]
    }
            
    return attribute_dict

if __name__ == "__main__":
    main()