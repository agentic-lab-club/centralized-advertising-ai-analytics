import React, { useState } from 'react';

function MLDashboards() {
  const [activeTab, setActiveTab] = useState('roi-forecast');

  const dashboards = [
    {
      id: 'roi-forecast',
      title: 'ROI Forecast by Channel',
      image: '/roi_forecast_by_channel.png',
      description: 'ML-predicted ROI performance by advertising channel'
    },
    {
      id: 'monthly-trends',
      title: 'Monthly ROI & CTR Trends',
      image: '/monthly_rois_and_ctr.png', 
      description: 'Historical trends and seasonal patterns analysis'
    }
  ];

  return (
    <div className="ml-dashboards">
      <div className="dashboard-header">
        <h2>ML Analytics Dashboards</h2>
        <div className="refresh-indicator">
          <span className="pulse-dot"></span>
          Auto-refresh: 30min
        </div>
      </div>

      <div className="dashboard-tabs">
        {dashboards.map(dashboard => (
          <button
            key={dashboard.id}
            className={`tab-button ${activeTab === dashboard.id ? 'active' : ''}`}
            onClick={() => setActiveTab(dashboard.id)}
          >
            {dashboard.title}
          </button>
        ))}
      </div>

      <div className="dashboard-content">
        {dashboards.map(dashboard => (
          <div
            key={dashboard.id}
            className={`dashboard-panel ${activeTab === dashboard.id ? 'active' : ''}`}
          >
            <div className="dashboard-info">
              <h3>{dashboard.title}</h3>
              <p>{dashboard.description}</p>
            </div>
            <div className="dashboard-image">
              <img 
                src={dashboard.image} 
                alt={dashboard.title}
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <div className="image-fallback" style={{display: 'none'}}>
                Dashboard image loading...
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MLDashboards;
