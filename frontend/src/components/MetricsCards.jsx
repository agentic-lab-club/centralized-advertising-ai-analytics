import React from 'react';
import { channelData } from '../data/hardcodedData';

function MetricsCards() {
  const totalROI = channelData.reduce((sum, ch) => sum + ch.roi, 0);
  const avgROI = totalROI / channelData.length;
  const avgConversion = channelData.reduce((sum, ch) => sum + ch.conversion_rate, 0) / channelData.length;
  const avgCost = channelData.reduce((sum, ch) => sum + ch.acquisition_cost, 0) / channelData.length;
  const topChannel = channelData.reduce((max, ch) => ch.roi > max.roi ? ch : max);

  const metrics = [
    {
      title: 'Average ROI',
      value: avgROI.toFixed(2),
      change: '+12.5%',
      trend: 'up',
      icon: 'ROI'
    },
    {
      title: 'Avg Conversion Rate',
      value: `${(avgConversion * 100).toFixed(1)}%`,
      change: '+2.3%',
      trend: 'up',
      icon: 'CVR'
    },
    {
      title: 'Avg Acquisition Cost',
      value: `$${avgCost.toFixed(0)}`,
      change: '-5.2%',
      trend: 'down',
      icon: 'COST'
    },
    {
      title: 'Top Channel',
      value: topChannel.channel,
      change: `${topChannel.roi.toFixed(2)} ROI`,
      trend: 'up',
      icon: 'TOP'
    }
  ];

  return (
    <div className="metrics-grid">
      {metrics.map((metric, index) => (
        <div key={index} className="metric-card">
          <div className="metric-header">
            <span className="metric-icon">{metric.icon}</span>
            <h3>{metric.title}</h3>
          </div>
          <div className="metric-value">{metric.value}</div>
          <div className={`metric-change ${metric.trend}`}>
            {metric.trend === 'up' ? '↗' : '↘'} {metric.change}
          </div>
        </div>
      ))}
    </div>
  );
}

export default MetricsCards;
