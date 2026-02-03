import React, { useState } from 'react';
import axios from 'axios';
import StockChart from './StockChart';
import Metrics from './Metrics';
import AISummary from './AISummary';

const Dashboard = () => {
    const [ticker, setTicker] = useState('AAPL');
    const [data, setData] = useState(null);
    const [info, setInfo] = useState(null);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchData = async () => {
        if (!ticker) return;
        setLoading(true);
        setError('');
        try {
            // Use relative path for proxy
            const response = await axios.get(`/api/stock/${ticker}`);
            setData(response.data.data);
            setInfo(response.data.info);
            setSummary(response.data.summary);
        } catch (err) {
            console.error(err);
            setError('Failed to fetch data. Please check the ticker symbol.');
            setData(null);
            setInfo(null);
            setSummary(null);
        }
        setLoading(false);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') fetchData();
    };

    return (
        <div className="container py-4">
            <header className="mb-5 text-center">
                <h1 className="display-4 fw-bold text-primary">📈 Stock Analyst</h1>
                <p className="lead text-muted">AI-Powered Technical & Fundamental Analysis</p>
            </header>

            {/* Search Bar */}
            <div className="row justify-content-center mb-5">
                <div className="col-md-6">
                    <div className="input-group input-group-lg">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Enter Stock Ticker (e.g., AAPL, TSLA)"
                            value={ticker}
                            onChange={(e) => setTicker(e.target.value)}
                            onKeyPress={handleKeyPress}
                        />
                        <button
                            className="btn btn-primary"
                            type="button"
                            onClick={fetchData}
                            disabled={loading}
                        >
                            {loading ? 'Analyzing...' : 'Analyze'}
                        </button>
                    </div>
                    {error && <div className="text-danger mt-2 text-center">{error}</div>}
                </div>
            </div>

            {/* Content */}
            {data && (
                <>
                    <AISummary summary={summary} />
                    <Metrics info={info} />
                    <StockChart data={data} ticker={ticker.toUpperCase()} />
                </>
            )}
        </div>
    );
};

export default Dashboard;
