# preprocess_csvs.py
import os, glob
import pandas as pd

DATA_DIR = "../data"
OUT_DIR = "./preprocessed"
os.makedirs(OUT_DIR, exist_ok=True)

def make_report_text(row):
    parts = []
    # common column names; adjust to your CSVs
    if "age" in row and pd.notna(row["age"]):
        parts.append(f"Age: {row['age']}")
    if "sex" in row and pd.notna(row.get("sex","")):
        parts.append(f"Sex: {row['sex']}")
    # symptoms: try common names
    sympt_cols = [c for c in row.index if "symptom" in c.lower() or "symptoms" in c.lower() or "pt_symptom" in c.lower()]
    sympts = []
    for c in sympt_cols:
        val = row.get(c)
        if pd.notna(val) and str(val).strip():
            sympts.append(str(val))
    if sympts:
        parts.append("Symptoms: " + ", ".join(sympts))
    # narrative columns if available
    for narrative_col in ["narrative","symptom_text","remarks","description","history"]:
        if narrative_col in row.index and pd.notna(row[narrative_col]):
            parts.append(str(row[narrative_col]))
            break
    return ". ".join(parts).strip()

def process_all_csvs():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    if not csv_files:
        print("No CSV files found in", DATA_DIR)
        return
    for csv_path in csv_files:
        print("Processing:", csv_path)
        try:
            df = pd.read_csv(csv_path, encoding='latin1', low_memory=False)
        except Exception:
            df = pd.read_csv(csv_path, encoding='utf-8', errors='ignore', low_memory=False)
        df.columns = [c.lower() for c in df.columns]
        # Ensure some id column exists
        if "id" not in df.columns and "vaers_id" in df.columns:
            df = df.rename(columns={"vaers_id":"id"})
        # Create report_text
        df["report_text"] = df.apply(make_report_text, axis=1)
        out_name = os.path.splitext(os.path.basename(csv_path))[0]
        out_path = os.path.join(OUT_DIR, f"preprocessed_{out_name}.csv")
        df.to_csv(out_path, index=False)
        print("Wrote:", out_path)

if __name__ == "__main__":
    process_all_csvs()
