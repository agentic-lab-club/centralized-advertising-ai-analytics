import React from 'react';

const AlertPanel = ({ alerts, onMarkRead }) => {
  if (!alerts || alerts.length === 0) {
    return null;
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return '🚨';
      case 'high': return '⚠️';
      case 'medium': return '⚡';
      case 'low': return 'ℹ️';
      default: return '📢';
    }
  };

  return (
    <div className="alert-panel">
      <div className="alert-header">
        <h3>🚨 Active Alerts ({alerts.length})</h3>
      </div>
      
      <div className="alert-list">
        {alerts.slice(0, 5).map(alert => (
          <div key={alert.id} className={`alert-item alert-${alert.severity}`}>
            <span className="alert-icon">{getSeverityIcon(alert.severity)}</span>
            <div className="alert-content">
              <strong>{alert.channel}</strong>: {alert.message}
            </div>
            <span className="alert-time">
              {new Date(alert.created_at).toLocaleTimeString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertPanel;
