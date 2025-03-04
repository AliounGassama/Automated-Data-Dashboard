import yfinance as yf
import pandas as pd
import os

# Function to fetch stock data
def fetch_stock_data(tickers, period, interval):
    for ticker in tickers:
        print(f"\nFetching data for {ticker}...")

        try:
            # Download stock data
            stock_data = yf.download(ticker, period=period, interval=interval)

            if stock_data.empty:
                print(f"No data found for {ticker}. Skipping...")
                continue

            # Reset index (move date from index to column)
            stock_data.reset_index(inplace=True)

            # Save data
            save_path = f"data/raw/{ticker}_data.csv"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            stock_data.to_csv(save_path, index=False)

            print(f"Data saved at {save_path}")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

# Function to validate tickers
def tickers_validation():
    while True:
        tickers = input("Enter stock tickers (comma-separated, e.g., AAPL, TSLA, MSFT): ").upper().split(",")
        tickers = [ticker.strip() for ticker in tickers if ticker.strip()]

        valid_tickers = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                if stock.history(period="1d").empty:
                    print(f"Warning: {ticker} might be invalid!")
                else:
                    valid_tickers.append(ticker)
            except:
                print(f"Invalid ticker: {ticker}")
        
        if valid_tickers:
            return valid_tickers
        else:
            print("No valid tickers provided. Please try again.")

# Function to validate period
def period_validation():
    while True:
        valid_periods = ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]
        period = input("Enter period (e.g., 1mo, 3mo, 1y, max): ").strip()

        if period in valid_periods:
            return period
        else:
            print(f"Invalid period! Choose from: {', '.join(valid_periods)}")

# Dictionary of vaild intervals for a given period
valid_intervals_by_period = {
    "1d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"],
    "5d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"],
    "1mo": ["5m", "15m", "30m", "60m", "90m", "1h", "1d"],
    "3mo": ["1h", "1d", "5d", "1wk"],
    "6mo": ["1d", "5d", "1wk", "1mo"],
    "1y": ["1d", "5d", "1wk", "1mo"],
    "2y": ["1d", "5d", "1wk", "1mo"],
    "5y": ["1d", "5d", "1wk", "1mo", "3mo"],
    "10y": ["1d", "5d", "1wk", "1mo", "3mo"],
    "ytd": ["1d", "5d", "1wk", "1mo"],
    "max": ["1d", "5d", "1wk", "1mo", "3mo"]
}

# Function to validate interval
def interval_validation(period):
    while True:
        valid_intervals = valid_intervals_by_period.get(period, [])
        interval = input("Enter interval (e.g., 1d, 1h, 5m): ").strip()
        
        if interval in valid_intervals:
            return interval
        else:
            print(f"Invalid interval! Choose from: {', '.join(valid_intervals)}")


# Run the function
if __name__ == "__main__":
    # Get user input for tickers (comma-separted)
    tickers = tickers_validation()

    # Get user input for period
    period = period_validation()

    # Get user input for interval
    interval = interval_validation(period)

    # Fetch and save stock data
    fetch_stock_data([ticker.strip() for ticker in tickers], period, interval)