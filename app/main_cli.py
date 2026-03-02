import logging
import sys
import os

# Add the project root and app directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.phase_1_data.dataset_loader import ZomatoLoader
from app.phase_2_input.input_handler import InputHandler
from app.phase_3_search.search_engine import RestaurantSearchEngine
from app.phase_4_llm.gemini_client import GoogleAIRecommendationClient
from app.phase_5_display.formatter import RestaurantFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    print("\n" + "="*50)
    print("Welcome to Zomato Restaurant Recommendation Service")
    print("="*50 + "\n")

    try:
        # Phase 1: Data Acquisition
        logger.info("Phase 1: Loading and cleaning Zomato dataset...")
        loader = ZomatoLoader()
        df = loader.get_structured_data()
        
        valid_locations = df["location"].dropna().unique().tolist()
        input_handler = InputHandler(valid_locations=valid_locations)
        search_engine = RestaurantSearchEngine()
        llm_client = GoogleAIRecommendationClient()
        formatter = RestaurantFormatter()

        while True:
            try:
                # Phase 2: User Input Handling
                logger.info("Phase 2: Capturing user preferences...")
                preferences = input_handler.get_user_preferences()
                
                # Check for quit signal
                if preferences["location"] is None:
                    print("\nExiting application. Goodbye!")
                    break
                
                # Phase 3: Search Logic
                logger.info(f"Phase 3: Searching for matches in {preferences['location']}...")
                results_df = search_engine.search(
                    df, 
                    preferences['location'], 
                    preferences['max_price'],
                    preferences.get('limit', 10)
                )
                
                # Phase 4: LLM Integration
                ai_summary = ""
                if not results_df.empty:
                    logger.info("Phase 4: Generating AI recommendation summary...")
                    ai_summary = llm_client.generate_summary(results_df)
                else:
                    logger.warning("No matches found. Skipping LLM summary.")
                
                # Phase 5: Result Display
                logger.info("Phase 5: Formatting and displaying results...")
                final_output = formatter.format_results(results_df, ai_summary)
                
                print(final_output)
                print("\n" + "="*50)
                print("Ready for another recommendation!")
                print("="*50 + "\n")
            except Exception as e:
                logger.error(f"An error occurred during search: {e}")
                print("\nSomething went wrong with that search. Let's try again.")
                print("="*50 + "\n")

    except KeyboardInterrupt:
        print("\n\nExiting application. Goodbye!")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print("\nSomething went wrong. Please check your configuration and try again.")

if __name__ == "__main__":
    main()
