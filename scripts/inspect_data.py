import os
import pandas as pd

RAW_DIR = "data/raw"
OUT = "summary_report.md"

def main():
    # load your dataset (replace filename if different)
    file = os.path.join(RAW_DIR, "GlobalWeatherRepository.csv")  
    df = pd.read_csv(file, low_memory=False)

    # basic info
    n_rows, n_cols = df.shape
    dtypes = df.dtypes.astype(str).to_dict()
    missing = (df.isna().sum() / n_rows * 100).sort_values(ascending=False)

    # try to find date column
    date_cols = [c for c in df.columns if "date" in c.lower()]
    date_range = None
    if date_cols:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors="coerce")
        date_range = (df[date_cols[0]].min(), df[date_cols[0]].max())

    # write summary
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# Data Inspection Summary\n\n")
        f.write(f"- Rows: {n_rows}\n- Columns: {n_cols}\n\n")
        f.write("## Data Types\n")
        for k,v in dtypes.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n## Missing Values (%)\n")
        for k,v in missing.items():
            if v > 0:
                f.write(f"- {k}: {v:.2f}%\n")
        if date_range:
            f.write(f"\n## Date Range\n- {date_range[0]} → {date_range[1]}\n")

    print("Summary written to summary_report.md")

if __name__ == "__main__":
    main()
