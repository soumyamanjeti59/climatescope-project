import os
import pandas as pd
import numpy as np

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

def main():
    file = os.path.join(RAW_DIR, "GlobalWeatherRepository.csv")
    df = pd.read_csv(file, low_memory=False)

    # 1. Parse dates
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # 2. Drop duplicates
    df = df.drop_duplicates()

    # 3. Handle missing
    num_cols = df.select_dtypes(include=[np.number]).columns
    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())
    obj_cols = df.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        df[c] = df[c].fillna("unknown")

    # 4. Unit conversion (example: Kelvin to Celsius)
    if "temperature" in df.columns:
        if df["temperature"].dropna().min() > 180:  # probably Kelvin
            df["temperature_c"] = df["temperature"] - 273.15

    # 5. Aggregate daily → monthly
    date_cols = [c for c in df.columns if "date" in c.lower()]
    if date_cols:
        df = df.set_index(date_cols[0])
        monthly = df.resample("M").mean(numeric_only=True)
        monthly.reset_index(inplace=True)
        monthly.to_csv(os.path.join(PROCESSED_DIR, "monthly_avg.csv"), index=False)

    # Save cleaned dataset
    df.to_csv(os.path.join(PROCESSED_DIR, "cleaned_weather.csv"), index=False)

    print("Cleaned and monthly aggregated data saved.")

if __name__ == "__main__":
    main()
