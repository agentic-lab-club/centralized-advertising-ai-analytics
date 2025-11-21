import os
import json
import requests
from dotenv import load_dotenv

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

# Основная функция
def get_llm_analytics_hf(user_prompt: str) -> str:
    """
    Отправляет user_prompt вместе с системным PROMPT в HuggingFace Qwen2.5-7B-Instruct.
    Возвращает текст JSON с рекомендациями.
    backend должен вызывать эту функцию, передавая подготовленные данные.
    
    user_prompt: str
        Строка JSON, содержащая данные каналов и вывод ML.
    """
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