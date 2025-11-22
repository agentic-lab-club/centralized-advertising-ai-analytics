import React from 'react';
import { budgetRecommendations } from '../data/hardcodedData';

function BudgetRecommendations() {
  return (
    <div className="budget-recommendations">
      <div className="section-header">
        <h2>AI Budget Recommendations</h2>
        <span className="ml-badge">ML Powered</span>
      </div>

      <div className="recommendations-table">
        <div className="table-header">
          <div>Channel</div>
          <div>Current Cost</div>
          <div>Predicted ROI</div>
          <div>Recommended Budget</div>
          <div>Change</div>
        </div>

        {budgetRecommendations.map((rec, index) => {
          const budgetChange = ((rec.recommended_budget - rec.acquisition_cost) / rec.acquisition_cost * 100);
          const isIncrease = budgetChange > 0;
          
          return (
            <div key={index} className="table-row">
              <div className="channel-cell">
                <span className="channel-icon">
                  {rec.channel === 'Instagram' ? 'IG' : 
                   rec.channel === 'Twitter' ? 'TW' :
                   rec.channel === 'Facebook' ? 'FB' : 'PT'}
                </span>
                {rec.channel}
              </div>
              <div>${rec.acquisition_cost.toLocaleString()}</div>
              <div className="roi-cell">
                <span className={`roi-value ${rec.roi_pred > 2 ? 'good' : 'poor'}`}>
                  {rec.roi_pred.toFixed(2)}
                </span>
              </div>
              <div className="budget-cell">
                ${rec.recommended_budget.toLocaleString()}
              </div>
              <div className={`change-cell ${isIncrease ? 'increase' : 'decrease'}`}>
                {isIncrease ? '↗' : '↘'} {Math.abs(budgetChange).toFixed(1)}%
              </div>
            </div>
          );
        })}
      </div>

      <div className="recommendations-summary">
        <div className="summary-item">
          <strong>Total Recommended Budget:</strong> 
          ${budgetRecommendations.reduce((sum, rec) => sum + rec.recommended_budget, 0).toLocaleString()}
        </div>
        <div className="summary-item">
          <strong>Expected ROI Improvement:</strong> 
          <span className="improvement">+15-20%</span>
        </div>
      </div>
    </div>
  );
}

export default BudgetRecommendations;
