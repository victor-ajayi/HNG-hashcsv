# HNG-hashcsv

**DISCLAIMER**: This script assumes the input CSV contains the data from all the teams and has 3 fields namely: `Serial Number`, `Filename`, `UUID`

Algorithm
1. Open CSV file
2. Iterate through file
3. Make JSON from each row
4. Create SHA256 hash from JSON
5. Create the output CSV file
6. Write row from input CSV + hash (in a new column)
6. Output the new CSV file as <originalfilename.output.csv>

```
Usage: python hash.py <csv name>
```