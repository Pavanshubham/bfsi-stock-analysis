import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. DATA HANDLING
# ==========================================

# Load the datasets using pandas
# (Make sure the dataset folder is in the same directory as this script)
print("Loading datasets...")
infy_df = pd.read_csv('dataset/INFY.NS.csv')
rel_df = pd.read_csv('dataset/Reliance.csv')
tcs_df = pd.read_csv('dataset/TCS_stock_history.csv')

# Function to clean the data
def clean_data(df):
    # Convert 'Date' column to proper datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Handle missing values by dropping rows with NaNs
    df.dropna(inplace=True)
    
    # Sort by date just in case
    df.sort_values('Date', inplace=True)
    
    # Set the Date column as the index for easier plotting
    df.set_index('Date', inplace=True)
    return df

# Apply cleaning to all datasets
infy_df = clean_data(infy_df)
rel_df = clean_data(rel_df)
tcs_df = clean_data(tcs_df)

print("Data Cleaning Complete.\n")

# ==========================================
# 2. STOCK ANALYSIS
# ==========================================

def analyze_stock(df, name):
    # Calculate Daily Returns: (Today's Close / Yesterday's Close) - 1
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    # Calculate Moving Averages (7-day and 30-day)
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    
    # Identify trend based on the last 30 days
    # We compare the most recent 30-day MA with the 30-day MA from 30 days ago
    recent_ma = df['MA_30'].iloc[-1]
    past_ma = df['MA_30'].iloc[-30]
    
    trend = "Stable"
    if recent_ma > past_ma * 1.02:  # If it grew by more than 2%
        trend = "Increasing"
    elif recent_ma < past_ma * 0.98: # If it fell by more than 2%
        trend = "Decreasing"
        
    # Calculate performance metrics for insights
    avg_return = df['Daily_Return'].mean()
    risk_std = df['Daily_Return'].std() # Standard deviation represents risk
    total_growth = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
    
    return {
        'Stock': name,
        'Avg_Daily_Return(%)': round(avg_return, 3),
        'Risk_Volatility(%)': round(risk_std, 3),
        'Total_Growth(%)': round(total_growth, 2),
        'Current_Trend': trend
    }

# Perform analysis on all three stocks
print("Performing Stock Analysis...")
infy_stats = analyze_stock(infy_df, 'Infosys')
rel_stats = analyze_stock(rel_df, 'Reliance')
tcs_stats = analyze_stock(tcs_df, 'TCS')

# Print the comparison
comparison_df = pd.DataFrame([infy_stats, rel_stats, tcs_stats])
print("\n--- Stock Comparison Table ---")
print(comparison_df.to_string(index=False))
print("------------------------------\n")

# ==========================================
# 3. VISUALIZATION
# ==========================================

print("Generating Visualizations...")

# Chart 1: Line chart (Date vs Close Price) for all 3 stocks.
# Since Prices might be on different scales historically, we'll plot recent data (last 3 years).
# Note: For your project, adjust the slice if datasets end on different dates.
plt.figure(figsize=(12, 6))
plt.plot(infy_df.index, infy_df['Close'], label='Infosys', linewidth=1.5)
plt.plot(rel_df.index, rel_df['Close'], label='Reliance', linewidth=1.5)
plt.plot(tcs_df.index, tcs_df['Close'], label='TCS', linewidth=1.5)

plt.title('Stock Close Price Comparison (Historical)')
plt.xlabel('Date')
plt.ylabel('Close Price (INR)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('stock_price_comparison.png') # Saves the image for your report
plt.show()

# Chart 2: Moving average chart for a specific stock (e.g., Reliance)
# Zooming in on the last 365 days for a clear view
rel_recent = rel_df.last("365D")

plt.figure(figsize=(12, 6))
plt.plot(rel_recent.index, rel_recent['Close'], label='Reliance Close Price', color='black', alpha=0.5)
plt.plot(rel_recent.index, rel_recent['MA_7'], label='7-Day Moving Average', color='blue', linewidth=2)
plt.plot(rel_recent.index, rel_recent['MA_30'], label='30-Day Moving Average', color='red', linewidth=2)

plt.title('Reliance Stock: Close Price vs Moving Averages (Last 1 Year)')
plt.xlabel('Date')
plt.ylabel('Price (INR)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('reliance_moving_averages.png') # Saves the image for your report
plt.show()

print("Analysis and Visualization complete. Check the generated PNG files.")
