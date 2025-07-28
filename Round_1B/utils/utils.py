import json

def load_persona_job(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "persona" in data and "job_to_be_done" in data:
                return data
    except Exception as e:
        print(f"Error reading persona_job.json: {e}")
    return None
