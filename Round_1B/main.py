import os
import json
import sys
import datetime
from utils.pdf_processor import extract_sections_from_pdfs
from utils.relevance_ranker import rank_sections
from utils.utils import load_persona_job

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
PERSONA_JSON = os.path.join(INPUT_DIR, "persona_job.json")

def main():
    if not os.path.exists(PERSONA_JSON):
        print(f"Missing persona_job.json in {INPUT_DIR}", file=sys.stderr)
        sys.exit(1)
    
    persona_job = load_persona_job(PERSONA_JSON)
    if not persona_job:
        print("Failed to load persona/job JSON.", file=sys.stderr)
        sys.exit(1)
    
    sections = extract_sections_from_pdfs(INPUT_DIR)
    if not sections:
        print("No sections extracted from input PDFs.", file=sys.stderr)
        sys.exit(1)
    
    ranked_sections = rank_sections(sections, persona_job)

    metadata = {
        "input_documents": sorted({sec['document'] for sec in sections}),
        "persona": persona_job.get("persona", ""),
        "job_to_be_done": persona_job.get("job_to_be_done", ""),
        "processing_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    output_json = {
        "metadata": metadata,
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    for rank, sec in enumerate(ranked_sections, start=1):
        output_json["extracted_sections"].append({
            "document": sec["document"],
            "page": sec["page"],
            "section_title": sec["title"],
            "importance_rank": rank
        })
        output_json["subsection_analysis"].append({
            "document": sec["document"],
            "page": sec["page"],
            "refined_text": sec["text"]
        })
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "challenge1b_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)
    
    print(f"Processing complete. Output saved: {output_path}")

if __name__ == "__main__":
    main()
