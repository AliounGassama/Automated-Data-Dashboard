import yfinance as yf
import pandas as pd
import os

# Function to clean data
def clean_stock_data():
    raw_data_path = "data/raw"
    processed_data_path = "data/processed"

    # Ensure the processed data directory exists
    os.makedirs(processed_data_path, exist_ok=True)

    files = [f for f in os.listdir(raw_data_path) if f.endswith(".csv")]

    for file in files:
        file_path = os.path.join(raw_data_path, file)
        print(f"Cleaning data in {file}...")

        try:
            # Read CSV with missing value handled
            df = pd.read_csv(file_path, na_values=["NA", "?", "-", "NaN"], parse_dates=["Date"])

            # Check if required columns exist
            required_columns = {"Date", "Open", "High", "Low", "Close"}
            missing_columns = required_columns - set(df.columns)

            if missing_columns:
                print(f"Warning: {file} is missing columns: {', '.join(missing_columns)}. Skipping...")
                continue

            # Drop duplicates
            df.drop_duplicates(inplace=True)

            # Save cleaned data
            save_path = os.path.join(processed_data_path, file)
            df.to_csv(save_path, index=False)

            print(f"Successfully cleaned data in {file}")
            
        except Exception as e:
            print(f"Failed to clean data in {file}: {e}")

if __name__ == "__main__":
    clean_stock_data()