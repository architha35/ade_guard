# batch_infer_ollama.py
import os, glob, json, time, requests, pandas as pd

PRE_DIR = "./preprocessed"
OUT_PATH = "../output/adeguard_results.jsonl"
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL = "phi3:mini"
SLEEP = 0.15   # seconds between calls

def build_prompt(report_text):
    # Clear instruction + ask for JSON only
    return f"""You are a clinical NLP assistant.
Extract and return JSON ONLY with keys:
- symptoms: list of strings
- severity: one of [mild, moderate, severe, unknown]
- duration: string or null
- age: number or null

Example:
Report: "Age: 45. Symptoms: fever and headache for 2 days."
Output: {{"symptoms":["fever","headache"], "severity":"mild", "duration":"2 days", "age":45}}

Now process this report:
Report: \"\"\"{report_text}\"\"\""""

def call_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    r = requests.post(OLLAMA_API, json=payload, timeout=90)
    r.raise_for_status()
    # Ollama often returns a JSON structure; try to extract text
    data = r.json()
    # Try several keys where text might be
    text_candidates = []
    if isinstance(data, dict):
        for k in ("response","output","text","result"):
            if k in data:
                text_candidates.append(data[k])
    if not text_candidates:
        text_candidates.append(json.dumps(data))
    # try to parse first candidate as JSON
    for txt in text_candidates:
        if isinstance(txt, dict):
            return txt
        try:
            return json.loads(txt)
        except Exception:
            # if not JSON, return raw string
            return {"raw": txt}
    return {"raw": str(data)}

def main():
    os.makedirs("../output", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fout:
        for csv_file in glob.glob(os.path.join(PRE_DIR, "preprocessed_*.csv")):
            print("Inferencing file:", csv_file)
            df = pd.read_csv(csv_file, low_memory=False)
            for idx, row in df.iterrows():
                text = row.get("report_text", "")
                if not isinstance(text, str) or len(text.strip()) < 5:
                    continue
                prompt = build_prompt(text)
                try:
                    model_out = call_ollama(prompt)
                except Exception as e:
                    model_out = {"error": str(e)}
                record = {
                    "source": os.path.basename(csv_file),
                    "index": int(idx),
                    "report_text": text,
                    "model_output": model_out
                }
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                # small sleep to avoid saturating model
                time.sleep(SLEEP)
    print("Saved results to", OUT_PATH)

if __name__ == "__main__":
    main()
