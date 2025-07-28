import os
import json
import sys
from utils.heading_extractor import extract_outline_from_pdf

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"


def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_json = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_json)
            try:
                title, outline = extract_outline_from_pdf(input_path)
                result = {
                    "title": title,
                    "outline": outline
                }
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Failed on {filename}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
