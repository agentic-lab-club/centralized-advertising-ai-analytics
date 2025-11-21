import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import AlertPanel from './components/AlertPanel';
import MetricsCards from './components/MetricsCards';
import './App.css';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [analytics, setAnalytics] = useState(null);
  const [channels, setChannels] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      console.log('Fetching data from API...');
      setError(null);
      
      // Fetch analytics summary
      const analyticsRes = await axios.get(`${API_URL}/analytics/summary`);
      setAnalytics(analyticsRes.data);

      // Fetch channel stats
      const channelsRes = await axios.get(`${API_URL}/analytics/channels`);
      setChannels(channelsRes.data);

      // Fetch recommendations
      try {
        const recRes = await axios.get(`${API_URL}/recommendations/latest`);
        setRecommendations(recRes.data);
      } catch (recError) {
        console.log('No recommendations available yet');
        setRecommendations(null);
      }

      // Fetch alerts
      try {
        const alertsRes = await axios.get(`${API_URL}/alerts/unread`);
        setAlerts(alertsRes.data);
      } catch (alertError) {
        console.log('No alerts available yet');
        setAlerts([]);
      }

      setLastUpdate(new Date());
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data from API. Make sure the backend is running.');
      setLoading(false);
    }
  };

  const markAlertAsRead = async (alertId) => {
    try {
      await axios.patch(`${API_URL}/alerts/${alertId}/read`);
      setAlerts(alerts.filter(alert => alert.id !== alertId));
    } catch (error) {
      console.error('Error marking alert as read:', error);
    }
  };

  useEffect(() => {
    fetchData();
    // Poll every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <h2>Loading DEMETRA Analytics...</h2>
        <p>Connecting to AI-powered dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-state">
        <div className="error-icon">⚠️</div>
        <h2>Connection Error</h2>
        <p>{error}</p>
        <button onClick={fetchData} className="retry-button">
          🔄 Retry Connection
        </button>
      </div>
    );
  }

  // Prepare data for pie chart
  const pieData = channels.map(channel => ({
    name: channel.channel,
    value: channel.avg_roi,
    campaigns: channel.total_campaigns
  }));

  const COLORS = ['#1a73e8', '#34a853', '#fbbc04', '#ea4335', '#9aa0a6'];

  return (
    <div className="App">
      <header className="header">
        <div className="header-content">
          <h1>🚀 DEMETRA SYSTEMS</h1>
          <h2>AI-Powered Advertising Analytics Dashboard</h2>
          <div className="header-stats">
            <div className="stat-item">
              <span className="stat-label">Total Campaigns</span>
              <span className="stat-value">{analytics?.total_campaigns || 0}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Top Channel</span>
              <span className="stat-value">{analytics?.top_performing_channel || 'N/A'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Last Updated</span>
              <span className="stat-value">{lastUpdate.toLocaleTimeString()}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Alerts Panel */}
      <AlertPanel alerts={alerts} onMarkRead={markAlertAsRead} />

      {/* KPI Cards */}
      {analytics && (
        <section className="kpi-section">
          <h3>📊 Key Performance Indicators</h3>
          <MetricsCards analytics={analytics} />
        </section>
      )}

      {/* Charts Section */}
      <section className="charts-section">
        <h3>📈 Performance Analytics</h3>
        <div className="charts-grid">
          <div className="chart-container">
            <h4>ROI by Channel</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={channels}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="channel" />
                <YAxis />
                <Tooltip formatter={(value) => [value.toFixed(2), 'ROI']} />
                <Bar dataKey="avg_roi" fill="#1a73e8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="chart-container">
            <h4>Conversion Rate by Channel</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={channels}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="channel" />
                <YAxis />
                <Tooltip formatter={(value) => [`${(value * 100).toFixed(2)}%`, 'Conversion Rate']} />
                <Bar dataKey="avg_conversion_rate" fill="#34a853" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container">
            <h4>ROI Distribution</h4>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value.toFixed(1)}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [value.toFixed(2), 'ROI']} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container">
            <h4>Campaign Volume by Channel</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={channels}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="channel" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="total_campaigns" fill="#fbbc04" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Channel Stats Table */}
      <section className="table-section">
        <h3>🎯 Detailed Channel Performance</h3>
        <div className="table-container">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Channel</th>
                <th>Campaigns</th>
                <th>Avg ROI</th>
                <th>Conversion Rate</th>
                <th>Total Clicks</th>
                <th>Total Impressions</th>
                <th>Avg Cost</th>
                <th>Performance</th>
              </tr>
            </thead>
            <tbody>
              {channels.map(channel => {
                const performance = channel.avg_roi > 2 ? 'Excellent' : 
                                 channel.avg_roi > 1.5 ? 'Good' : 
                                 channel.avg_roi > 1 ? 'Average' : 'Poor';
                
                return (
                  <tr key={channel.channel}>
                    <td className="channel-name">
                      {channel.channel.replace('_', ' ').toUpperCase()}
                    </td>
                    <td>{channel.total_campaigns}</td>
                    <td className={channel.avg_roi > 2 ? 'good' : channel.avg_roi > 1 ? 'ok' : 'bad'}>
                      {channel.avg_roi.toFixed(2)}
                    </td>
                    <td>{(channel.avg_conversion_rate * 100).toFixed(2)}%</td>
                    <td>{channel.total_clicks.toLocaleString()}</td>
                    <td>{channel.total_impressions.toLocaleString()}</td>
                    <td>${channel.avg_acquisition_cost.toFixed(0)}</td>
                    <td className={`performance-${performance.toLowerCase()}`}>
                      {performance}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* AI Recommendations */}
      {recommendations && recommendations.summary && (
        <section className="recommendations-section">
          <h3>🤖 AI-Powered Insights & Recommendations</h3>
          <div className="recommendations-container">
            <div className="recommendation-card main-summary">
              <h4>📋 Executive Summary</h4>
              <p>{recommendations.summary}</p>
            </div>
            
            {recommendations.channel_comparison && (
              <div className="recommendation-card">
                <h4>📊 Channel Analysis</h4>
                <div className="json-display">
                  {typeof recommendations.channel_comparison === 'object' ? 
                    Object.entries(recommendations.channel_comparison).map(([key, value]) => (
                      <div key={key} className="json-item">
                        <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : value}
                      </div>
                    )) :
                    <p>{recommendations.channel_comparison}</p>
                  }
                </div>
              </div>
            )}
            
            {recommendations.recommendations && (
              <div className="recommendation-card">
                <h4>💡 Action Items</h4>
                <div className="json-display">
                  {typeof recommendations.recommendations === 'object' ? 
                    Object.entries(recommendations.recommendations).map(([key, value]) => (
                      <div key={key} className="json-item">
                        <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : value}
                      </div>
                    )) :
                    <p>{recommendations.recommendations}</p>
                  }
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Quick Actions */}
      <section className="actions-section">
        <h3>⚡ Quick Actions</h3>
        <div className="actions-grid">
          <button className="action-button" onClick={fetchData}>
            🔄 Refresh Data
          </button>
          <button className="action-button" onClick={() => window.print()}>
            📄 Export Report
          </button>
          <button className="action-button" onClick={() => {
            const data = { analytics, channels, recommendations };
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `demetra-analytics-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
          }}>
            💾 Download Data
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>DEMETRA SYSTEMS</h4>
            <p>AI Analytics Dashboard © 2024</p>
          </div>
          <div className="footer-section">
            <h4>Performance Summary</h4>
            <p>Top Channel: <strong>{analytics?.top_performing_channel}</strong></p>
            <p>Total Campaigns: <strong>{analytics?.total_campaigns}</strong></p>
          </div>
          <div className="footer-section">
            <h4>System Status</h4>
            <p>Status: <span className="status-online">🟢 Online</span></p>
            <p>Last Sync: {lastUpdate.toLocaleString()}</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
