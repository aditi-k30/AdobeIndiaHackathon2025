import fitz  # PyMuPDF
import re
from collections import Counter

HEADING_KEYWORDS = {
    "en": [r"^chapter\s+\d+", r"^section\s+\d+", r"^\d+(\.\d+)*\s", r"^appendix"],
    "ja": [r"^第[一二三四五六七八九十百千0-9]+[章節]", r"^章", r"^節"]
}


def regex_match_any(patterns, text):
    for pat in patterns:
        if re.match(pat, text, re.IGNORECASE):
            return True
    return False


def guess_title(page):
    blocks = page.get_text("dict")["blocks"]
    text_spans = []
    for b in blocks:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip():
                    text_spans.append(s)
    if not text_spans:
        return "Untitled"
    font_sizes = [round(s["size"], 1) for s in text_spans]
    size_counter = Counter(font_sizes)
    most_common_size = size_counter.most_common(1)[0][0]
    big_spans = [s for s in text_spans if s["size"] > most_common_size + 2]
    if big_spans:
        big_spans.sort(key=lambda s: s["bbox"][1])
        candidate = big_spans[0]
    else:
        text_spans.sort(key=lambda s: (-s["size"], s["bbox"][1]))
        candidate = text_spans[0]
    return candidate["text"].strip()


def detect_heading_level(text, size, fontname, size_bins, lang):
    levels = sorted(size_bins.keys(), reverse=True)
    text_clean = text.strip()
    if not text_clean:
        return None
    if re.match(r"^(table of contents|index|references|bibliography)$", text_clean, re.IGNORECASE):
        return "H1"

    if regex_match_any(HEADING_KEYWORDS.get("en", []), text_clean.lower()):
        bin_ = size_bins.get(size)
        if bin_ == 0:
            return "H1"
        elif bin_ == 1:
            return "H2"
        else:
            return "H3"

    if regex_match_any(HEADING_KEYWORDS.get("ja", []), text_clean):
        bin_ = size_bins.get(size)
        if bin_ == 0:
            return "H1"
        elif bin_ == 1:
            return "H2"
        else:
            return "H3"

    is_bold = "Bold" in fontname or "bold" in fontname
    is_caps = text_clean.isupper() and len(text_clean) > 3
    bin_ = size_bins.get(size)
    if bin_ == 0 and (is_bold or is_caps or len(text_clean) < 80):
        return "H1"
    if bin_ == 1 and (is_bold or len(text_clean) < 70):
        return "H2"
    if bin_ == 2 and len(text_clean) < 60:
        return "H3"
    return None


def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_spans = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    s_text = s["text"].strip()
                    if not s_text:
                        continue
                    all_spans.append({
                        "text": s_text,
                        "size": round(s["size"], 1),
                        "font": s.get("font", ""),
                        "page": page_num + 1,
                        "y0": s["bbox"][1]
                    })

    all_spans = [
        s for s in all_spans
        if len(s["text"]) > 2 and not re.match(r"^[\s\.\-\–—•·]+$", s["text"])
    ]
    if not all_spans:
        return ("Untitled", [])

    title_page = doc[0]
    title = guess_title(title_page)

    sizes = [s["size"] for s in all_spans]
    filtered_sizes = [sz for sz in sizes if 7 < sz < 48]
    header_sizes = sorted(set(filtered_sizes), reverse=True)[:5]
    size_bins = {sz: idx for idx, sz in enumerate(header_sizes)}

    en_count = sum(1 for s in all_spans[:50] if re.search(r"[A-Za-z]", s["text"]))
    ja_count = sum(1 for s in all_spans[:50] if re.search(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]", s["text"]))
    lang = "en" if en_count >= ja_count else "ja"

    outline = []
    for s in all_spans:
        lvl = detect_heading_level(s["text"], s["size"], s["font"], size_bins, lang)
        if lvl:
            if not (lvl == "H3" and re.match(r"^\d+\.\d+(\.\d+)*\s", s["text"])):
                outline.append({"level": lvl, "text": s["text"], "page": s["page"]})

    unique = []
    seen = set()
    for h in outline:
        key = (h["level"], h["text"].strip().lower(), h["page"])
        if key not in seen:
            seen.add(key)
            unique.append(h)
    return (title, unique)
