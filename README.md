# 📈 BFSI Project: Stock Market & Mutual Fund Analysis

This is an end-to-end Python web application built with Streamlit for analyzing and predicting stock market trends, as well as providing insights into Mutual Funds. It's designed to be a comprehensive submission for a BFSI (Banking, Financial Services, and Insurance) college project.

**🚀 Live Demo:** [Replace this with your Streamlit Cloud Link]

## 🌟 Features

- **Interactive UI**: Clean sidebar navigation switching between Stock Analysis and Mutual Funds.
- **Dynamic File Uploader**: Upload any historical Stock CSV file directly from the UI.
- **KPI Dashboards**: Autocalculates highest, lowest, and current Close prices.
- **Technical Indicators**: Interactively evaluates 7-Day and 30-Day Moving Averages.
- **Machine Learning**: Utilizes Scikit-learn's Linear Regression to predict a 30-day future price trend.
- **Automated Insights**: Generates simple-English financial insights reading market sentiment (Bullish/Bearish) and volatility (Risk).
- **Mutual Fund Comparison**: A structured breakdown comparing risk/reward ratios of standard mutual fund categories.

## 🛠️ Tech Stack

- **Python 3.x**
- **Streamlit** (Frontend UI)
- **Pandas** (Data Manipulation)
- **Matplotlib** (Graph Visualization)
- **Scikit-Learn** (Predictive Modeling)

## 📁 Project Structure

```text
bfsi-mini/
├── app.py                  # Main Streamlit application file
├── requirements.txt        # Required python dependencies deployment file
├── README.md               # Project documentation
└── dataset/                # Folder containing CSVs
    ├── INFY.NS.csv
    ├── Reliance.csv
    └── TCS_stock_history.csv
```

## 💻 How to Run Locally

1. Clone or download this repository.
2. Open your terminal/command prompt.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
5. Open your web browser using the `localhost` URL provided in the terminal.

## ☁️ Deployment Instructions (Streamlit Cloud)

1. Upload this entire project folder to a public GitHub repository.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub and click **New app**.
4. Select your repository, set branch to `main`, and main file path to `app.py`.
5. Click **Deploy!**

---
*Created for a BFSI Data Science Academic Project.*
