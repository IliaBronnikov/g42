import csv
import re
from datetime import datetime, timezone

import dateparser
import phonenumbers

UAE_CC = "+971"
INPUT_FILE = "input_data.csv"
OUTPUT_FILE = "normalized_contacts.csv"
DATE_PARS_SETTINGS = {
    "DATE_ORDER": "DMY",
    "PREFER_DAY_OF_MONTH": "first",
    "PARSERS": ["timestamp", "relative-time", "absolute-time", "custom-formats"],
    "STRICT_PARSING": True,
}


def clean_phone_number(raw_phone: str) -> str:
    """
    Phone processing function
    """

    # clean common format error
    phone = raw_phone.lower()
    phone = re.sub(r"[oO]", "0", phone)
    phone = re.sub(r"[^\d+]", "", phone)

    if phone.startswith("0"):  # process UAE local numbers 0 -> +971
        phone = UAE_CC + phone[1:]
    elif phone.startswith("00"):  # process 00 to international number
        phone = "+" + phone[2:]
    elif not phone.startswith("+"):
        phone = "+" + phone

    try:
        region = None

        if phone.startswith(UAE_CC):
            region = "AE"

        parsed = phonenumbers.parse(phone, region)

        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number")

        formatted = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.E164
        )

        return formatted
    except Exception as e:
        raise ValueError(f"Phone parse error: {e}")


def normalize_date(raw_date: str) -> str:
    """
    Date processing function
    """

    raw = raw_date.strip()

    dt = dateparser.parse(raw, settings=DATE_PARS_SETTINGS)

    if dt is None:
        DATE_PARS_SETTINGS["DATE_ORDER"] = "MDY"
        dt = dateparser.parse(raw, settings=DATE_PARS_SETTINGS)

    if dt is None:
        raise ValueError("Invalid date format")

    year = dt.year
    if year < 100:
        if year <= 25:
            year += 2000
        else:
            year += 1900
        dt = dt.replace(year=year)

    return dt.strftime("%Y-%m-%d")


def main():
    start_time = datetime.now(timezone.utc).replace(microsecond=0)

    print(f"Starting processing file {INPUT_FILE} - {start_time}")

    processed = 0
    normalized = 0
    skipped = 0
    reasons = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as rf, open(
        OUTPUT_FILE, "w", newline="", encoding="utf-8"
    ) as wf:

        reader = csv.DictReader(rf, delimiter=";")
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(wf, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for row in reader:
            processed += 1
            row_id = row["id"]
            phone_raw = row["phone"]
            dob_raw = row["dob"]

            try:
                phone_norm = clean_phone_number(phone_raw)
                dob_norm = normalize_date(dob_raw)
                writer.writerow({"id": row_id, "phone": phone_norm, "dob": dob_norm})
                normalized += 1
            except Exception as e:
                skipped += 1
                reasons.append(f"id={row_id}: {e}")

            if processed % 50 == 0:
                print(f"Processed {processed} rows")

    print(f"Processing file {INPUT_FILE} done.")
    print(
        f"Process time - {(datetime.now(timezone.utc) - start_time).seconds} sec", "\n"
    )
    print(f"Processed rows: {processed}")
    print(f"Successfully normalized: {normalized}")
    print(f"Skipped rows: {skipped}", "\n")
    if reasons:
        print("Reasons for skipping:")
        for r in reasons:
            print(" -", r)


if __name__ == "__main__":
    main()
