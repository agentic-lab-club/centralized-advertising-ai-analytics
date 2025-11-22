import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.hf_api_key = os.getenv("HF_API_KEY")
        self.hf_api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
        
        self.prompt_template = """
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
    
    def get_llm_analytics_hf(self, user_prompt: str) -> Dict[str, Any]:
        """
        Send user_prompt with system PROMPT to HuggingFace Qwen2.5-7B-Instruct.
        Returns JSON with recommendations.
        """
        if not self.hf_api_key:
            return self._mock_recommendation()
        
        headers = {
            "Authorization": f"Bearer {self.hf_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"{self.prompt_template}\n\nUSER DATA:\n{user_prompt}",
            "parameters": {"temperature": 0.2, "max_new_tokens": 700}
        }

        try:
            response = requests.post(self.hf_api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and "generated_text" in data[0]:
                generated_text = data[0]["generated_text"]
                # Extract JSON from response
                json_start = generated_text.find('{')
                json_end = generated_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    return json.loads(generated_text[json_start:json_end])
            
            return self._mock_recommendation()
        
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._mock_recommendation()
    
    def generate_recommendations(self, analytics_data: Dict, ml_predictions: Dict) -> Dict[str, Any]:
        """Generate AI recommendations based on analytics and ML predictions"""
        
        user_data = {
            "analytics": analytics_data,
            "ml_predictions": ml_predictions
        }
        
        user_prompt = json.dumps(user_data, indent=2)
        return self.get_llm_analytics_hf(user_prompt)
    
    def _mock_recommendation(self) -> Dict[str, Any]:
        """Fallback mock recommendation for MVP"""
        return {
            "channel_comparison": {
                "top_channel": "google_ads",
                "analysis": "Google Ads shows highest ROI. Facebook needs optimization."
            },
            "ml_predictions": {
                "trend": "ROI expected to increase by 15% with current strategy"
            },
            "recommendations": {
                "budget_allocation": "Increase Google Ads budget by 20%",
                "optimization": "Reduce spend on underperforming channels"
            },
            "summary": "Overall performance is positive. Focus on top channels and optimize creatives."
        }
