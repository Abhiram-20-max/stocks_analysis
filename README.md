#  AI-Powered Stock Analysis Platform

A full-stack financial analysis application that combines real-time stock data, technical indicators, and AI-driven insights to help users make informed investment decisions.

##  Overview

This project is a modern web application built to analyze stock market performance. It fetches live data, calculates key technical indicators (RSI, lipid, MACD, SMA), and uses an AI agent to generate natural-language performance summaries.

**Highlights:**
- **Real-time Data**: Fetches live stock data using Yahoo Finance.
- **Interactive Charts**: Responsive Candlestick charts with RSI and Moving Average overlays using Plotly.js.
- **AI Analyst**: Generates automated textual commentary on stock trends and technical signals.
- **Dockerized**: Fully containerized for easy deployment.

##  Tech Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: Flask
- **Data Source**: `yfinance`
- **Analysis**: `pandas` (SMA, RSI, MACD calculation)

### Frontend
- **Framework**: React (Vite)
- **Styling**: Bootstrap 5
- **Visualization**: `plotly.js`, `react-plotly.js`

### DevOps
- **Containerization**: Docker & Docker Compose

##  Getting Started

### Option 1: Docker (Recommended)
Prerequisite: Docker Desktop installed.

Set your Alpha Vantage API key (optional fallback when Yahoo Finance fails):

```bash
set ALPHAVANTAGE_API_KEY=your_key_here
```

```bash
# Clone the repository
git clone https://github.com/yourusername/stocks-analysis.git
cd stocks-analysis

# Build and Run
docker-compose up --build
```
Access the app at `http://localhost:5173`.

### Option 2: Manual Setup
If you don't have Docker, you can run the services individually.

**1. Backend**
```bash
cd backend
pip install -r requirements.txt
set ALPHAVANTAGE_API_KEY=your_key_here
python run.py
# Server starts at http://localhost:5000
```

**2. Frontend**
```bash
cd frontend
npm install
npm run dev
# App starts at http://localhost:5173
```

##  Features

- **Dashboard**: Search for any stock ticker (e.g., AAPL, NVDA, TSLA).
- **Technical Analysis**:
  - **SMA 50 & 200**: Identify long-term trends and potential crossovers.
  - **RSI (14)**: Spot overbought (>70) or oversold (<30) conditions.
  - **MACD**: Gauge momentum and trend direction.
- **Fundamental Metrics**: View P/E Ratio, Earnings Growth, and Sector info.
- **AI Summary**: Get a quick, readable paragraph summarizing the technical outlook.

##  License
This project is open-source and available under the MIT License.
