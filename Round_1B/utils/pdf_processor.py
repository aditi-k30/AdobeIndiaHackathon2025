import fitz  # PyMuPDF
import os
import re

SECTION_HEADER_PATTERNS = [
    re.compile(r"^\d+(\.\d+)*\s+.+"),
    re.compile(r"^[IVXLCDM]+\.\s+.+", re.IGNORECASE),
]

def is_section_heading(text):
    text = text.strip()
    if len(text) < 3:
        return False
    for pattern in SECTION_HEADER_PATTERNS:
        if pattern.match(text):
            return True
    if text.isupper() and len(text) < 50:
        return True
    return False

def extract_sections_from_pdfs(input_dir):
    sections = []
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    for pdf_file in pdf_files:
        path = os.path.join(input_dir, pdf_file)
        try:
            doc_sections = extract_sections_from_pdf(path, pdf_file)
            sections.extend(doc_sections)
        except Exception as e:
            print(f"Warning: Failed to process {pdf_file}: {e}")
    return sections

def extract_sections_from_pdf(pdf_path, pdf_filename):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if not text:
                continue
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if is_section_heading(line):
                    title = line.strip()
                    body_lines = lines[i+1:] if i+1 < len(lines) else []
                    body_text = "\n".join(body_lines).strip()
                    if len(body_text) < 20:
                        body_text = ""
                    sections.append({
                        "document": pdf_filename,
                        "page": page_num + 1,
                        "title": title,
                        "text": body_text if body_text else title
                    })
    if not sections:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text().strip()
            if text:
                sections.append({
                    "document": pdf_filename,
                    "page": page_num + 1,
                    "title": f"Page {page_num + 1}",
                    "text": text
                })
    return sections
