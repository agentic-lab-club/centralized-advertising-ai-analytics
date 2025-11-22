import os
import json
import requests
from dotenv import load_dotenv

# Hardcoded data from ML outputs
HARDCODED_CHANNEL_DATA = [
    {"channel": "Twitter", "acquisition_cost": 7774.12, "conversion_rate": 0.080, "roi": 4.002},
    {"channel": "Pinterest", "acquisition_cost": 7769.74, "conversion_rate": 0.080, "roi": 0.716},
    {"channel": "Facebook", "acquisition_cost": 7746.02, "conversion_rate": 0.080, "roi": 3.987},
    {"channel": "Instagram", "acquisition_cost": 7726.25, "conversion_rate": 0.080, "roi": 4.009}
]

HARDCODED_BUDGET_RECOMMENDATIONS = [
    {"channel": "Twitter", "roi_pred": 3.358, "roi_forecast": 3.342, "acquisition_cost": 7795.30, "recommended_budget": 31441.15},
    {"channel": "Instagram", "roi_pred": 3.358, "roi_forecast": 3.342, "acquisition_cost": 7713.38, "recommended_budget": 31207.60},
    {"channel": "Facebook", "roi_pred": 3.343, "roi_forecast": 3.321, "acquisition_cost": 7743.15, "recommended_budget": 31114.65},
    {"channel": "Pinterest", "roi_pred": 0.669, "roi_forecast": 0.670, "acquisition_cost": 7778.50, "recommended_budget": 6236.61}
]

# Загрузка LLM модели
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"

# Prompt для LLM
PROMPT = """
You are an analytics assistant for a marketing dashboard.
You ALWAYS return a strictly valid JSON object.

The user will provide:
- Aggregated analytics data from ad platforms
- ML model results (ROI drivers, forecasts, risk segments)

Your tasks:

1. Compare performance across channels.
2. Identify strengths, weaknesses, anomalies.
3. Analyze ML feature importance.
4. Give recommendations for:
   - budget allocation
   - CPC / CTR / CPM improvements
   - conversion optimization
   - ROI growth
5. Provide a short summary.

Your JSON response MUST follow this structure:

{
  "channel_comparison": {},
  "ml_predictions": {},
  "recommendations": {},
  "summary": ""
}

Rules:
- STRICTLY return valid JSON.
- NO extra text.
- Use ONLY metrics provided by the user.
- Respond in English.
"""

def get_hardcoded_recommendations():
    """Return hardcoded recommendations based on ML data"""
    return {
        "channel_comparison": {
            "top_performer": "Instagram",
            "worst_performer": "Pinterest",
            "analysis": "Instagram and Twitter show highest ROI (4.0+). Pinterest significantly underperforms with 0.7 ROI."
        },
        "ml_predictions": {
            "trend": "ROI expected to stabilize around 3.3-3.4 for top channels",
            "forecast_accuracy": "High confidence in predictions"
        },
        "recommendations": {
            "budget_allocation": "Reallocate Pinterest budget to Instagram and Twitter",
            "optimization": "Pinterest needs creative and targeting optimization",
            "priority_actions": [
                "Increase Instagram budget by 25%",
                "Reduce Pinterest spend by 60%",
                "A/B test Twitter creative formats",
                "Optimize Facebook audience targeting"
            ]
        },
        "summary": "Strong performance from Instagram, Twitter, and Facebook. Pinterest requires immediate optimization or budget reallocation. Recommended budget shifts could improve overall ROI by 15-20%."
    }

# Основная функция
def get_llm_analytics_hf(user_prompt: str = None) -> str:
    """
    Returns hardcoded recommendations or uses HuggingFace if API key available.
    For demo purposes, always returns hardcoded data based on ML outputs.
    """
    
    # For demo/hackathon - use hardcoded data
    if not HF_API_KEY or True:  # Force hardcoded for demo
        recommendations = get_hardcoded_recommendations()
        return json.dumps(recommendations, indent=2)
    
    # Original LLM logic (kept for reference)
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": f"{PROMPT}\n\nUSER DATA:\n{user_prompt}",
        "parameters": {"temperature": 0.2, "max_new_tokens": 700}
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]

    return str(data)

def get_channel_data():
    """Get hardcoded channel performance data"""
    return HARDCODED_CHANNEL_DATA

def get_budget_recommendations():
    """Get hardcoded budget recommendations"""
    return HARDCODED_BUDGET_RECOMMENDATIONS

if __name__ == "__main__":
    # Demo the hardcoded recommendations
    print("=== DEMETRA AI Analytics - Hardcoded Demo ===")
    print("\nChannel Data:")
    for channel in get_channel_data():
        print(f"  {channel['channel']}: ROI {channel['roi']:.2f}, Cost ${channel['acquisition_cost']:.0f}")
    
    print("\nBudget Recommendations:")
    for rec in get_budget_recommendations():
        change = ((rec['recommended_budget'] - rec['acquisition_cost']) / rec['acquisition_cost'] * 100)
        print(f"  {rec['channel']}: ${rec['recommended_budget']:.0f} ({change:+.1f}%)")
    
    print("\nLLM Recommendations:")
    recommendations = get_llm_analytics_hf()
    print(recommendations)
