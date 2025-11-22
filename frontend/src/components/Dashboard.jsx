import React from 'react';
import MetricsCards from './MetricsCards';
import MLDashboards from './MLDashboards';
import BudgetRecommendations from './BudgetRecommendations';
import AIRecommendations from './AIRecommendations';
import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>DEMETRA SYSTEMS</h1>
        <h2>AI Analytics Dashboard</h2>
        <div className="status-badge">
          <span className="status-dot"></span>
          Live ML Predictions
        </div>
      </header>

      <MetricsCards />
      
      <MLDashboards />
      
      <div className="recommendations-section">
        <BudgetRecommendations />
        <AIRecommendations />
      </div>
    </div>
  );
}

export default Dashboard;
