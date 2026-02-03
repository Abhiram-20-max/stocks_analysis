from flask import Blueprint, jsonify
from .services.data_service import get_stock_data
from .services.analysis_service import calculate_technical_indicators
from .services.ai_service import generate_summary

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/stock/<ticker>', methods=['GET'])
def stock_analysis(ticker):
    ticker = ticker.upper()
    
    # 1. Fetch Data
    raw_data = get_stock_data(ticker)
    if not raw_data:
        return jsonify({"error": f"Could not fetch data for {ticker}"}), 404
        
    history = raw_data['history']
    info = raw_data['info']
    
    # 2. Calculate Indicators
    analyzed_history = calculate_technical_indicators(history)
    
    # 3. Generate AI Summary
    summary = generate_summary(ticker, analyzed_history)
    
    return jsonify({
        "ticker": ticker,
        "info": info,
        "data": analyzed_history,
        "summary": summary
    })

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200
