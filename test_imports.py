import os
import sys

# Add the current directory to sys.path
sys.path.append(os.getcwd())

try:
    from app.phase_1_data.dataset_loader import ZomatoLoader
    from app.phase_3_search.search_engine import RestaurantSearchEngine
    from app.phase_4_llm.gemini_client import GoogleAIRecommendationClient
    print("SUCCESS: Core modules imported correctly from 'app' package.")
    
    loader = ZomatoLoader()
    print("SUCCESS: ZomatoLoader initialized.")
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
