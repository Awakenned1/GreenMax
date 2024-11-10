import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def generate_ai_recommendations(usage_data):
    try:
        prompt = f"""
        Based on this energy usage:
        - Current: {usage_data['current_power']} kW
        - Status: {usage_data['status']}
        - Time: {usage_data['timestamp']}

        Provide 3 specific energy-saving recommendations.
        """

        response = model.generate_content(prompt)
        return response.text.split('\n')[:3]
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return [
            "Reduce usage during peak hours",
            "Use energy-efficient appliances",
            "Monitor device consumption regularly"
        ]
