import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="BFSI Project: Stock & Mutual Fund Analysis", page_icon="📈", layout="wide")

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select Application Function", ["Stock Market Analysis", "Mutual Fund Analysis"])

# ==========================================
# HELPER FUNCTIONS
# ==========================================
@st.cache_data
def load_and_clean_data(filepath):
    """Loads CSV and converts Date column, handling any basic errors."""
    try:
        df = pd.read_csv(filepath)
        if 'Date' not in df.columns or 'Close' not in df.columns:
            st.error(f"File {filepath} is missing required 'Date' or 'Close' columns.")
            return None
            
        df['Date'] = pd.to_datetime(df['Date'])
        df.dropna(inplace=True)
        df.sort_values('Date', inplace=True)
        df.set_index('Date', inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return None

def predict_future_prices(df, days=30):
    """Predicts future prices using a simple Linear Regression model."""
    df_pred = df.copy()
    df_pred['Day_Index'] = np.arange(len(df_pred))
    
    X = df_pred[['Day_Index']]
    y = df_pred['Close']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict the next 'days' days
    future_indices = np.arange(len(df_pred), len(df_pred) + days).reshape(-1, 1)
    future_preds = model.predict(future_indices)
    
    # Create future dates
    last_date = df_pred.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)
    
    return pd.Series(future_preds, index=future_dates)

# ==========================================
# APP MODE: STOCK ANALYSIS
# ==========================================
if app_mode == "Stock Market Analysis":
    st.title("📈 Stock Market Analysis")
    st.markdown("Upload your historical stock datasets below to generate automated financial insights.")
    
    st.sidebar.header("📁 Upload Dataset")
    st.sidebar.info("Upload standard stock CSV files (Ensure columns: Date, Close, etc.)")
    uploaded_files = st.sidebar.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    
    # If users haven't uploaded, try to use default if available, otherwise ask to upload
    datasets = {}
    if uploaded_files:
        for file in uploaded_files:
            datasets[file.name] = file
    else:
        # Fallback to local files for testing if they exist in the dataset folder
        default_files = ['dataset/Reliance.csv', 'dataset/INFY.NS.csv', 'dataset/TCS_stock_history.csv']
        for file in default_files:
            if os.path.exists(file):
                filename = os.path.basename(file)
                datasets[filename] = file
                
    if not datasets:
        st.warning("⚠️ Please upload a CSV file from the sidebar to begin.")
    else:
        st.success(f"✅ Loaded {len(datasets)} dataset(s) for analysis.")
        
        # Dropdown to select stock
        selected_stock = st.selectbox("Select a stock to completely analyze:", list(datasets.keys()))
        
        # Load data
        df = load_and_clean_data(datasets[selected_stock])
        
        if df is not None:
            # --- KPI METRICS ---
            st.header(f"1️⃣ 📊 {selected_stock.replace('.csv', '')} Key Performance Indicators (KPIs)")
            
            latest_price = df['Close'].iloc[-1]
            highest_price = df['Close'].max()
            lowest_price = df['Close'].min()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Close Price", f"₹ {latest_price:.2f}")
            col2.metric("Highest Historical Price", f"₹ {highest_price:.2f}")
            col3.metric("Lowest Historical Price", f"₹ {lowest_price:.2f}")
            
            st.divider()
            
            # --- MOVING AVERAGES ---
            st.header("2️⃣ 📉 Trend Analysis (Moving Averages)")
            
            # Calculate Moving Averages
            df['7-Day MA'] = df['Close'].rolling(window=7).mean()
            df['30-Day MA'] = df['Close'].rolling(window=30).mean()
            
            # Visualizing the last year to keep it clean
            recent_df = df.tail(365)
            
            st.markdown("This chart compares the Close Price with 7-Day (Short Term) and 30-Day (Long Term) Moving Averages to identify momentum.")
            st.line_chart(recent_df[['Close', '7-Day MA', '30-Day MA']])
            
            st.divider()
            
            # --- PREDICTION (LINEAR REGRESSION) ---
            st.header("3️⃣ 🤖 Price Prediction (Linear Regression)")
            st.markdown("Using a basic Machine Learning model (Linear Regression) to predict the price trend for the next 30 days based on recent trajectory.")
            
            # Use last 1 year for training a more relevant recent trend
            train_data = df.tail(365) 
            future_predictions = predict_future_prices(train_data, days=30)
            
            # Plot historical vs predicted
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(train_data.index, train_data['Close'], label='Historical (Last 365 Days)', color='blue')
            ax.plot(future_predictions.index, future_predictions, label='Predicted (Next 30 Days)', color='red', linestyle='--')
            ax.set_title(f"30-Day Price Prediction for {selected_stock}")
            ax.set_xlabel('Date')
            ax.set_ylabel('Price (INR)')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)
            
            st.divider()
            
            # --- AUTO GENERATED INSIGHTS ---
            st.header("4️⃣ 💡 Automated Risk & Return Insights")
            
            df['Daily_Return'] = df['Close'].pct_change() * 100
            risk = df['Daily_Return'].std()
            total_return = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
            
            recent_ma = df['30-Day MA'].iloc[-1]
            past_ma = df['30-Day MA'].iloc[-30]
            if recent_ma > past_ma * 1.02:
                trend_status = "Bullish (Increasing)"
            elif recent_ma < past_ma * 0.98:
                trend_status = "Bearish (Decreasing)"
            else:
                trend_status = "Stable / Consolidation"
                
            st.info(f"""
            **In Simple English:**
            * **Market Trend:** The stock is currently in a **{trend_status}** phase over the last 30 days.
            * **Volatility (Risk):** The standard deviation of daily returns is **{risk:.2f}%**. A high number (above 2%) means the stock is very risky and volatile. A lower number means it is stable.
            * **Lifetime Growth:** Since the beginning of this dataset, the stock has grown by **{total_return:.2f}%**. 
            """)

# ==========================================
# APP MODE: MUTUAL FUND ANALYSIS
# ==========================================
elif app_mode == "Mutual Fund Analysis":
    st.title("💼 Mutual Fund Comparison")
    st.markdown("Mutual funds pool money from many investors to purchase a diversified portfolio of stocks and bonds. Below is a conceptual comparison of standard mutual fund categories.")
    
    st.header("1️⃣ Understanding Fund Categories")
    
    # Create standard mutual fund comparison data
    fund_data = {
        "Fund Category": ["Large Cap Equity", "Mid Cap Equity", "Small Cap Equity", "Debt Fund (Bonds)", "Hybrid (Balanced)"],
        "Target Companies": ["Top 100 Giant Companies (TCS, Reliance)", "Emerging Companies (Rank 101-250)", "New & Small Startups", "Government & Corporate Bonds", "Mix of Stocks & Bonds"],
        "Expected Return (Annual)": ["10% - 12%", "14% - 16%", "18% - 25%", "6% - 8%", "9% - 11%"],
        "Risk Level ": ["Moderate Risk", "High Risk", "Very High Risk", "Low Risk", "Moderate-Low Risk"],
        "Suitable Investor": ["Long-term, seeks stability", "Aggressive growth seekers", "Very aggressive, long-term", "Retirees, capital protection", "Beginners looking for balance"]
    }
    
    mf_df = pd.DataFrame(fund_data)
    st.table(mf_df)
    
    st.divider()
    
    st.header("2️⃣ Why Invest in Mutual Funds over Direct Stocks?")
    st.success("""
    **Conclusion & Insight:**
    While directly investing in a single stock (like Reliance, as seen in the Stock Analysis section) can yield massive returns, it also heavily increases your risk. If that one company fails, you lose your capital.
    
    Mutual Funds automatically apply the concept of **Diversification**. By spreading your money across 50-100 different companies, even if one sector falls, the others protect your investment. Choosing the right mutual fund allows an investor to balance their desired **Risk versus Reward**.
    """)
