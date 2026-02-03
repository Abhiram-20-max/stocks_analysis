import React from 'react';

const AISummary = ({ summary }) => {
    if (!summary) return null;

    return (
        <div className="card shadow-sm mb-4 border-info">
            <div className="card-header bg-info text-white">
                <h5 className="mb-0">AI Analyst Summary</h5>
            </div>
            <div className="card-body">
                <p className="card-text lead" style={{ fontSize: '1.1rem' }}>
                    🤖 {summary}
                </p>
            </div>
        </div>
    );
};

export default AISummary;
