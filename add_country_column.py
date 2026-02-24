"""
Add a 'country' column to affluence_*.csv files by extracting country from the prompt column.
Prompt template: 'photo of a _ in {country}'
Renames: United Arab Emirates -> UAE, United States of America -> United States
"""

import csv
import glob
import os

COUNTRY_RENAMES = {
    "United Arab Emirates": "UAE",
    "United States of America": "United States",
}

PROMPT_PREFIX = " in "  # country is the text after " in " in the prompt


def extract_country(prompt: str) -> str:
    """Extract country from prompt (template: '... in {country}')."""
    if PROMPT_PREFIX not in prompt:
        return ""
    return prompt.split(PROMPT_PREFIX, 1)[1].strip()


def normalize_country(country: str) -> str:
    """Apply standard renames for country names."""
    return COUNTRY_RENAMES.get(country, country)


def process_file(filepath: str) -> None:
    """Read CSV, add country column, write back."""
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        if "country" in fieldnames:
            print(f"  Skipping {filepath}: already has 'country' column")
            return
        # Insert 'country' after 'prompt'
        idx = fieldnames.index("prompt") + 1
        new_fieldnames = fieldnames[:idx] + ["country"] + fieldnames[idx:]
        for row in reader:
            raw_country = extract_country(row["prompt"])
            row["country"] = normalize_country(raw_country)
            rows.append(row)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Updated: {filepath}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(script_dir, "affluence_*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No affluence_*.csv files found in {script_dir}")
        return
    print(f"Processing {len(files)} file(s)...")
    for filepath in files:
        process_file(filepath)
    print("Done.")


if __name__ == "__main__":
    main()
