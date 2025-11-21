import React from 'react';

const MetricsCards = ({ analytics }) => {
  if (!analytics) return null;

  const metrics = [
    {
      title: 'Average ROI',
      value: analytics.avg_roi.toFixed(2),
      change: analytics.roi_change,
      icon: '📈',
      format: 'number'
    },
    {
      title: 'Conversion Rate',
      value: (analytics.avg_conversion_rate * 100).toFixed(2),
      change: analytics.conversion_change,
      icon: '🎯',
      format: 'percentage'
    },
    {
      title: 'Avg Cost per Acquisition',
      value: analytics.avg_acquisition_cost.toFixed(0),
      change: analytics.cost_change,
      icon: '💰',
      format: 'currency',
      inverse: true // Lower is better
    },
    {
      title: 'Total Clicks',
      value: analytics.total_clicks.toLocaleString(),
      change: analytics.clicks_change,
      icon: '👆',
      format: 'number'
    }
  ];

  const getChangeClass = (change, inverse = false) => {
    if (inverse) {
      return change <= 0 ? 'positive' : 'negative';
    }
    return change >= 0 ? 'positive' : 'negative';
  };

  const getChangeIcon = (change, inverse = false) => {
    if (inverse) {
      return change <= 0 ? '↗' : '↘';
    }
    return change >= 0 ? '↗' : '↘';
  };

  return (
    <div className="metrics-cards">
      {metrics.map((metric, index) => (
        <div key={index} className="metric-card">
          <div className="metric-header">
            <span className="metric-icon">{metric.icon}</span>
            <span className="metric-title">{metric.title}</span>
          </div>
          
          <div className="metric-value">
            {metric.format === 'currency' && '$'}
            {metric.value}
            {metric.format === 'percentage' && '%'}
          </div>
          
          <div className={`metric-change ${getChangeClass(metric.change, metric.inverse)}`}>
            {getChangeIcon(metric.change, metric.inverse)} {Math.abs(metric.change).toFixed(1)}%
          </div>
        </div>
      ))}
    </div>
  );
};

export default MetricsCards;
