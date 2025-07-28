# Adobe India Hackathon 2025 - Connecting the Dots Challenge

## Overview

This repository contains solutions for **Round 1A: PDF Outline Extraction** and **Round 1B: Persona-Driven Document Intelligence** of the Adobe India Hackathon 2025 “Connecting the Dots” challenge.

---

## Project Structure

├── Round_1A/
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ ├── README.md
│ └── utils/
│ └── heading_extractor.py
├── Round_1B/
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ ├── README.md
│ ├── approach_explanation.md
│ └── utils/
│ ├── pdf_processor.py
│ ├── relevance_ranker.py
│ └── utils.py
└── README.md (this file)


---

## Round 1A: PDF Outline Extraction

### Objective

Extract structured hierarchical outlines (title, H1/H2/H3 headings with page numbers) from PDF documents.

### How it works

- Uses **PyMuPDF** to parse PDFs.
- Detects headings using font sizes, styles, and regex patterns.
- Supports multi-language (English / Japanese) heading detection.
- Outputs a JSON file per PDF describing the document outline.

### Build & Run

1. Navigate to `Round_1A` folder.
2. Build the Docker image:

docker build --platform linux/amd64 -t round1a-extractor:latest .

3. Create an `input/` directory in `Round_1A` and place your PDF files there.
4. Run the container:

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a-extractor:latest

5. Find output JSON files inside `Round_1A/output/`.

---

## Round 1B: Persona-Driven Document Intelligence

### Objective

Extract and prioritize the most relevant sections from a collection of documents based on a persona and their job-to-be-done.

### How it works

- Parses PDFs into sections using **PyMuPDF** and heading heuristics.
- Processes persona and job descriptions as a combined textual query.
- Uses **TF-IDF vectorization and cosine similarity** for scoring and ranking sections by relevance.
- Outputs a JSON file with metadata, ranked sections, and refined subsections.

### Build & Run

1. Navigate to the `Round_1B` folder.
2. Build the Docker image:

docker build --platform linux/amd64 -t round1b-intelligence:latest 

3. Create an `input/` directory in `Round_1B/` and place 3-10 PDF files there.
4. Add a `persona_job.json` file inside the same `input/` folder with the format:

{
"persona": "Your persona description",
"job_to_be_done": "Your job-to-be-done description"
}

5. Run the container:

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b-intelligence:latest

6. Output JSON file named `challenge1b_output.json` will be saved inside `Round_1B/output/`.

---

## Common Notes

- Both solutions run **fully offline** and require **CPU-only** environments.
- Docker images are built with minimal dependencies and are compatible with linux/amd64 platform.
- Place your input PDFs and required JSON files inside respective `input/` folders before running.
- Outputs are saved in `output/` folders in the respective challenge directories.
- Ensure Docker is installed and running on your system.

---

## Dependencies

- Python 3.10+
- PyMuPDF
- scikit-learn (Round 1B only)
- numpy (Round 1B only)


---

Thank you for reviewing our submission for the Adobe India Hackathon 2025!
