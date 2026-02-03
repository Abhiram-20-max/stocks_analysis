import React from 'react';

const Metrics = ({ info }) => {
    if (!info) return null;

    return (
        <div className="card shadow-sm mb-4">
            <div className="card-body">
                <h5 className="card-title mb-3">Fundamental Metrics</h5>
                <div className="row text-center">
                    <div className="col-md-3">
                        <h6 className="text-muted">Sector</h6>
                        <p className="fw-bold">{info.sector}</p>
                    </div>
                    <div className="col-md-3">
                        <h6 className="text-muted">Price</h6>
                        <p className="fw-bold">
                            {info.summaryQuote ? info.summaryQuote.toFixed(2) : 'N/A'} {info.currency}
                        </p>
                    </div>
                    <div className="col-md-3">
                        <h6 className="text-muted">P/E Ratio</h6>
                        <p className="fw-bold">
                            {info.peRatio ? info.peRatio.toFixed(2) : 'N/A'}
                        </p>
                    </div>
                    <div className="col-md-3">
                        <h6 className="text-muted">Earnings Growth</h6>
                        <p className="fw-bold">
                            {info.earningsGrowth ? (info.earningsGrowth * 100).toFixed(2) + '%' : 'N/A'}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Metrics;
