import os
import logging
import json
import pandas as pd
from typing import Optional, Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class GroqRecommendationClient:
    """
    Phase 4: LLM Integration (Groq)
    Wraps Groq's API to provide AI-generated restaurant recommendation summaries.
    Now supports both overall and individual restaurant summaries.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("GROQ_API_KEY not found in environment. LLM features will be disabled.")
            self.client = None
        else:
            # Using Llama 3.3 70B
            self.client = Groq(api_key=self.api_key)
            self.model_name = "llama-3.3-70b-versatile"

    def generate_summary(self, recommendations: pd.DataFrame) -> Dict[str, Any]:
        """
        Generates structured summaries (overall + individual) using Groq's LLM.
        Returns a dictionary with 'overall_summary' and 'individual_summaries'.
        """
        default_response = {
            "overall_summary": "AI summary unavailable.",
            "individual_summaries": {}
        }

        if self.client is None:
            return default_response

        if recommendations.empty:
            default_response["overall_summary"] = "No restaurants found."
            return default_response

        # Use up to 5 recommendations for context
        top_recommendations = recommendations.head(5)
        logger.info(f"Generating summary for {len(top_recommendations)} restaurants using Groq...")
        prompt = self._build_prompt(top_recommendations)
        
        try:
            logger.info(f"Requesting structured summary from Groq ({self.model_name})...")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful Zomato restaurant recommendation assistant. "
                            "You must respond ONLY with a valid JSON object. "
                            "The JSON must have two keys: 'overall_summary' (a 2-3 sentence string) "
                            "and 'individual_summaries' (a dictionary where keys are restaurant names "
                            "and values are short 1-sentence specific insights about that restaurant)."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.7,
            )
            
            content = chat_completion.choices[0].message.content.strip()
            return json.loads(content)
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit_exceeded" in error_str.lower():
                logger.error("Groq API quota exceeded (429).")
                default_response["overall_summary"] = "QUOTA_EXCEEDED: Your Groq API limit has been reached."
                return default_response
            
            logger.error(f"Error generating summary from Groq: {e}")
            default_response["overall_summary"] = f"Failed to generate summary: {error_str}"
            return default_response

    def _build_prompt(self, df: pd.DataFrame) -> str:
        """
        Helper to construct the prompt string from the DataFrame.
        """
        restaurant_list = []
        for _, row in df.iterrows():
            resto_info = f"- {row['name']} | Location: {row['location']} | Cuisines: {row['cuisines']} | Rating: {row['rate']}/5 | Cost: {row['approx_cost(for two people)']}."
            restaurant_list.append(resto_info)
        
        context = "\n".join(restaurant_list)
        return (
            "Based on these restaurants, please provide:\n"
            "1. An overall summary of these choices.\n"
            "2. A unique 1-sentence insight for EACH restaurant listed below.\n\n"
            f"{context}"
        )

if __name__ == "__main__":
    # Quick sanity check with dummy data
    client = GroqRecommendationClient()
    dummy_rec = pd.DataFrame({
        "name": ["Empire Restaurant", "Corner House"],
        "location": ["Indiranagar", "Koramangala"],
        "rate": [4.2, 4.8],
        "approx_cost(for two people)": [800, 300],
        "cuisines": ["North Indian", "Ice Cream"]
    })
    
    print("Testing Groq Summary Generation:")
    result = client.generate_summary(dummy_rec)
    print(json.dumps(result, indent=2))
