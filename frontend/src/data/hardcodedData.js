// Hardcoded data from ML outputs
export const channelData = [
  {
    channel: "Twitter",
    acquisition_cost: 7774.12,
    conversion_rate: 0.080,
    roi: 4.002
  },
  {
    channel: "Pinterest", 
    acquisition_cost: 7769.74,
    conversion_rate: 0.080,
    roi: 0.716
  },
  {
    channel: "Facebook",
    acquisition_cost: 7745.02,
    conversion_rate: 0.080,
    roi: 3.987
  },
  {
    channel: "Instagram",
    acquisition_cost: 7726.25,
    conversion_rate: 0.080,
    roi: 4.009
  }
];

export const budgetRecommendations = [
  {
    channel: "Twitter",
    roi_pred: 3.358,
    roi_forecast: 3.342,
    acquisition_cost: 7795.30,
    recommended_budget: 31441.15
  },
  {
    channel: "Instagram",
    roi_pred: 3.358,
    roi_forecast: 3.342,
    acquisition_cost: 7713.38,
    recommended_budget: 31207.60
  },
  {
    channel: "Facebook",
    roi_pred: 3.343,
    roi_forecast: 3.321,
    acquisition_cost: 7743.15,
    recommended_budget: 31114.65
  },
  {
    channel: "Pinterest",
    roi_pred: 0.669,
    roi_forecast: 0.670,
    acquisition_cost: 7778.50,
    recommended_budget: 6236.61
  }
];

export const llmRecommendations = {
  channel_comparison: {
    top_performer: "Instagram",
    worst_performer: "Pinterest", 
    analysis: "Instagram and Twitter show highest ROI (4.0+). Pinterest significantly underperforms with 0.7 ROI."
  },
  ml_predictions: {
    trend: "ROI expected to stabilize around 3.3-3.4 for top channels",
    forecast_accuracy: "High confidence in predictions"
  },
  recommendations: {
    budget_allocation: "Reallocate Pinterest budget to Instagram and Twitter",
    optimization: "Pinterest needs creative and targeting optimization",
    priority_actions: [
      "Increase Instagram budget by 25%",
      "Reduce Pinterest spend by 60%", 
      "A/B test Twitter creative formats",
      "Optimize Facebook audience targeting"
    ]
  },
  summary: "Strong performance from Instagram, Twitter, and Facebook. Pinterest requires immediate optimization or budget reallocation. Recommended budget shifts could improve overall ROI by 15-20%."
};
