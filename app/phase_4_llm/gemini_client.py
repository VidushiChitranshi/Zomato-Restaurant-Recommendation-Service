import os
import logging
import pandas as pd
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class GoogleAIRecommendationClient:
    """
    Phase 4: LLM Integration (Google AI Studio)
    Wraps Google's Gemini API to provide AI-generated restaurant recommendation summaries.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found in environment. LLM features will be disabled.")
            self.client = None
        else:
            # Using Gemini 2.0 Flash
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = 'gemini-2.0-flash'

    def generate_summary(self, recommendations: pd.DataFrame) -> str:
        """
        Generates a summary of recommended restaurants using Google's Gemini LLM.
        """
        if self.client is None:
            return "AI summary unavailable (API key not configured)."

        if recommendations.empty:
            return "No restaurants were found matching your criteria, so no summary is available."

        # Take top 3 for the context to avoid token limits and stay concise
        top_recommendations = recommendations.head(3)
        
        prompt = self._build_prompt(top_recommendations)
        
        try:
            logger.info(f"Requesting summary from Google AI Studio ({self.model_name})...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=300,
                    temperature=0.7,
                )
            )
            return response.text.strip()
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                logger.error("Gemini API quota exceeded (429).")
                return "QUOTA_EXCEEDED: Your Gemini API free tier quota has been reached. Please wait a minute or check your Google AI Studio limits."
            
            logger.error(f"Error generating summary from Google AI: {e}")
            return f"Failed to generate AI summary: {error_str}"

    def _build_prompt(self, df: pd.DataFrame) -> str:
        """
        Helper to construct the prompt string from the DataFrame.
        """
        restaurant_list = []
        for _, row in df.iterrows():
            resto_info = f"- {row['name']} located in {row['location']}, serving {row['cuisines']}, with a rating of {row['rate']}/5. Cost for two: {row['approx_cost(for two people)']}."
            restaurant_list.append(resto_info)
        
        context = "\n".join(restaurant_list)
        return (
            "You are a helpful Zomato restaurant recommendation assistant. "
            "Please provide a 2-3 sentence summary of why these top restaurant choices are good, "
            "focusing on their cuisine and rating:\n\n"
            f"{context}"
        )

if __name__ == "__main__":
    # Quick sanity check with dummy data
    client = GoogleAIRecommendationClient()
    dummy_rec = pd.DataFrame({
        "name": ["Empire Restaurant", "Corner House"],
        "location": ["Indiranagar", "Koramangala"],
        "rate": [4.2, 4.8],
        "approx_cost(for two people)": [800, 300],
        "cuisines": ["North Indian", "Ice Cream"]
    })
    
    print("Testing Gemini Summary Generation:")
    if client.client:
        print(client.generate_summary(dummy_rec))
    else:
        print("Client not initialized (check GOOGLE_API_KEY)")
