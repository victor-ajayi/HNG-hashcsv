# HNG-hashcsv

**PLEASE NOTE**: This script assumes that the `Attributes` field is strictly formatted like so:
```
hair: burgundy cap; eyes: none; teeth: none; clothing: black and kente agbada; accessories: none;  expression: none; strength: none; weakness: none
```

Algorithm
1. Open CSV file
2. Iterate through file
3. Make JSON of each row
4. Create SHA256 hash from JSON
5. Create the output CSV file
6. Write row from input CSV + hash (in a new column)
6. Output the new CSV file as <originalfilename.output.csv>

```
Usage: python hash.py <csv name>
```