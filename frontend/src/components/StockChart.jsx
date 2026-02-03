import React from 'react';
import Plot from 'react-plotly.js';

const StockChart = ({ data, ticker }) => {
    if (!data || data.length === 0) return <div>No chart data available.</div>;

    const dates = data.map(item => item.Date);

    // Candlestick trace
    const candlestickTrace = {
        x: dates,
        close: data.map(item => item.Close),
        high: data.map(item => item.High),
        low: data.map(item => item.Low),
        open: data.map(item => item.Open),
        decreasing: { line: { color: '#ff4d4d' } },
        increasing: { line: { color: '#00cc66' } },
        line: { color: 'rgba(31,119,180,1)' },
        type: 'candlestick',
        xaxis: 'x',
        yaxis: 'y',
        name: 'Price'
    };

    // SMA 50
    const sma50Trace = {
        x: dates,
        y: data.map(item => item.SMA_50),
        type: 'scatter',
        mode: 'lines',
        line: { color: '#ff9900', width: 1.5 },
        name: 'SMA 50'
    };

    // SMA 200
    const sma200Trace = {
        x: dates,
        y: data.map(item => item.SMA_200),
        type: 'scatter',
        mode: 'lines',
        line: { color: '#0066cc', width: 1.5 },
        name: 'SMA 200'
    };

    // RSI Trace (Subplot)
    const rsiTrace = {
        x: dates,
        y: data.map(item => item.RSI),
        type: 'scatter',
        mode: 'lines',
        yaxis: 'y2',
        line: { color: '#9933cc', width: 1.5 },
        name: 'RSI'
    };

    // Layout
    const layout = {
        title: `${ticker} Analysis`,
        dragmode: 'zoom',
        showlegend: true,
        height: 700,
        grid: {
            rows: 2,
            columns: 1,
            pattern: 'independent',
            roworder: 'top to bottom'
        },
        xaxis: {
            rangeslider: { visible: false },
            autorange: true
        },
        yaxis: {
            autorange: true,
            domain: [0.35, 1],
            title: 'Price'
        },
        yaxis2: {
            autorange: true,
            domain: [0, 0.25],
            title: 'RSI',
            range: [0, 100]
        },
        // Shapes for RSI 30/70
        shapes: [
            {
                type: 'line',
                xref: 'x', yref: 'y2',
                x0: dates[0], y0: 70,
                x1: dates[dates.length - 1], y1: 70,
                line: { color: 'red', width: 1, dash: 'dot' }
            },
            {
                type: 'line',
                xref: 'x', yref: 'y2',
                x0: dates[0], y0: 30,
                x1: dates[dates.length - 1], y1: 30,
                line: { color: 'green', width: 1, dash: 'dot' }
            }
        ]
    };

    return (
        <div className="card shadow-sm p-3 mb-4">
            <Plot
                data={[candlestickTrace, sma50Trace, sma200Trace, rsiTrace]}
                layout={layout}
                useResizeHandler={true}
                style={{ width: '100%', height: '100%' }}
            />
        </div>
    );
};

export default StockChart;
