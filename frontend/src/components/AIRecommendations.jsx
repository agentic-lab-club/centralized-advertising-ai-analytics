import React from 'react';
import { llmRecommendations } from '../data/hardcodedData';

function AIRecommendations() {
  return (
    <div className="ai-recommendations">
      <div className="section-header">
        <h2>AI Insights & Recommendations</h2>
        <span className="llm-badge">LLM Powered</span>
      </div>

      <div className="recommendations-content">
        <div className="summary-section">
          <h3>Executive Summary</h3>
          <p className="summary-text">{llmRecommendations.summary}</p>
        </div>

        <div className="analysis-grid">
          <div className="analysis-card">
            <h4>Channel Performance</h4>
            <div className="performance-item">
              <span className="label">Top Performer:</span>
              <span className="value good">{llmRecommendations.channel_comparison.top_performer}</span>
            </div>
            <div className="performance-item">
              <span className="label">Needs Attention:</span>
              <span className="value poor">{llmRecommendations.channel_comparison.worst_performer}</span>
            </div>
            <p className="analysis-text">{llmRecommendations.channel_comparison.analysis}</p>
          </div>

          <div className="analysis-card">
            <h4>ML Predictions</h4>
            <div className="prediction-item">
              <span className="trend-indicator">TREND</span>
              <span>{llmRecommendations.ml_predictions.trend}</span>
            </div>
            <div className="prediction-item">
              <span className="confidence-indicator">CONF</span>
              <span>{llmRecommendations.ml_predictions.forecast_accuracy}</span>
            </div>
          </div>
        </div>

        <div className="action-items">
          <h4>Priority Actions</h4>
          <div className="actions-list">
            {llmRecommendations.recommendations.priority_actions.map((action, index) => (
              <div key={index} className="action-item">
                <span className="action-number">{index + 1}</span>
                <span className="action-text">{action}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="key-recommendations">
          <div className="rec-item">
            <h5>Budget Strategy</h5>
            <p>{llmRecommendations.recommendations.budget_allocation}</p>
          </div>
          <div className="rec-item">
            <h5>Optimization Focus</h5>
            <p>{llmRecommendations.recommendations.optimization}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIRecommendations;
