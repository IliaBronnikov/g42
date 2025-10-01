# CSV Contact Normalizer

## Overview
This Python script reads a CSV file containing contact information with columns `id;phone;dob`, normalizes phone numbers to the E.164 format, and dates of birth (dob) to ISO 8601 format (`YYYY-MM-DD`). It outputs a new CSV file with the normalized data.

- Phone numbers without country code but starting with 0 are assumed to be UAE numbers and prefixed with +971 after removing the leading 0.
- Dates are parsed intelligently supporting multiple formats and two-digit years with a pivot year of 25.

## Example Input (input_data.csv)
id;phone;dob

U001;971542719583;02.01.1990

U002;058_510_8603;Apr-05-2004

U003;+1-415-555-2671;5.22.1997

## Example Output (normalized_contacts.csv)
id;phone;dob

U001;+971542719583;1990-01-02

U002;+971585108603;2004-04-05

U003;+14155552671;1997-05-22

## Example logs during process
Starting processing file input_data.csv - 2025-09-22 11:11:11

Processed 50 rows

Processed 100 rows

Processing file input_data.csv done.

Process time - 10 sec 

Processed rows: 110

Successfully normalized: 108

Skipped rows: 2

Reasons for skipping:
 - id=U005: Phone parse error: Invalid phone number
 - id=U009: Phone parse error: Invalid phone number

## Requirements
- Python 3.13+
- Packages: `phonenumbers`, `dateparser`

## How to Run

### Using Python directly

```python
python normalize_contacts.py
```

The script expects `input_data.csv` in the same directory and creates `normalized_contacts.csv`.

### Using Docker

1. Build the Docker image:

```
docker build -t normalize_contacts .
```

2. Run the container (mount current directory to `/app` inside container):
```
docker run --rm -v $(pwd):/app normalize_contacts
```
This command runs the script inside a container, reading `input_data.csv` and writing `normalized_contacts.csv` to your current directory.
