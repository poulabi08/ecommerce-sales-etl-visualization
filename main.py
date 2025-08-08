from etl.extract import extract_from_csv
from etl.transform import transform_orders as transform
# from etl.load import load_to_postgres  # Uncomment this when ready to load

import pandas as pd
import logging
import os

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_summary(df, name=""):
    print(f"\n📊 Summary for {name}")
    print("Shape:", df.shape)
    print("Nulls:\n", df.isnull().sum())
    print("Types:\n", df.dtypes)
    logging.info(f"{name} Shape: {df.shape}")
    logging.info(f"{name} Nulls: {df.isnull().sum().to_dict()}")
    logging.info(f"{name} Dtypes: {df.dtypes.to_dict()}")

def run_etl():
    df_raw = extract_from_csv('Data/orders.csv')
    print("✅ Data Extracted")
    print(df_raw.head())
    logging.info("✅ Data Extracted")

    generate_summary(df_raw, "Raw Data")

    df_clean = transform(df_raw)
    print("✅ Data Transformed")
    print(df_clean.head())
    logging.info("✅ Data Transformed")

    generate_summary(df_clean, "Cleaned Data")

    # Save cleaned data to CSV
    output_path = 'Data/cleaned_orders.csv'
    df_clean.to_csv(output_path, index=False)
    print(f"✅ Cleaned Data Saved to {output_path}")
    logging.info(f"✅ Cleaned Data Saved to {output_path}")

    # Uncomment the line below when PostgreSQL is ready
    # load_to_postgres(df_clean)
    print("✅ Data Loaded to PostgreSQL")
    logging.info("✅ Data Loaded to PostgreSQL")

if __name__ == "__main__":
    run_etl()
