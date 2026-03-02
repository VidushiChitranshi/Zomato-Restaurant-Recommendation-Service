import os
import sys

# Add the project root and app directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

from app.phase_1_data.dataset_loader import ZomatoLoader
from app.phase_3_search.search_engine import RestaurantSearchEngine
from app.phase_4_llm.gemini_client import GoogleAIRecommendationClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Zomato Recommendation Service API")

# Global instances for reuse
loader = ZomatoLoader()
search_engine = RestaurantSearchEngine()
llm_client = GoogleAIRecommendationClient()

# Cache the dataset in memory
df = loader.get_structured_data()

class RecommendationRequest(BaseModel):
    location: str
    max_price: float
    limit: int = 10

class RestaurantInfo(BaseModel):
    name: str
    rate: float
    approx_cost: float
    cuisines: str
    location: str

class RecommendationResponse(BaseModel):
    restaurants: List[RestaurantInfo]
    ai_summary: str

@app.get("/api/locations")
async def get_locations():
    """Returns the list of unique locations from the dataset."""
    try:
        locations = sorted(df["location"].dropna().unique().tolist())
        return {"locations": locations}
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching locations.")

@app.post("/api/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    """Orchestrates search and AI summary for the given preferences."""
    logger.info(f"Received recommendation request: {request}")
    try:
        results_df = search_engine.search(
            df, 
            request.location, 
            request.max_price, 
            request.limit
        )
        
        restaurants = []
        for _, row in results_df.iterrows():
            restaurants.append(RestaurantInfo(
                name=row['name'],
                rate=row['rate'],
                approx_cost=row['approx_cost(for two people)'],
                cuisines=row['cuisines'],
                location=row['location']
            ))
            
        ai_summary = ""
        if restaurants:
            ai_summary = llm_client.generate_summary(results_df)
        
        return RecommendationResponse(
            restaurants=restaurants,
            ai_summary=ai_summary
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating recommendations.")

# Mount static files
static_path = os.path.join(os.getcwd(), "app", "phase_6_web", "static")
if not os.path.exists(static_path):
    # Fallback to relative if cwd is already in phase_6_web
    static_path = os.path.join(os.path.dirname(__file__), "static")

if os.path.exists(static_path):
    logger.info(f"Serving static files from {static_path}")
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
else:
    logger.error(f"Static directory not found at {static_path}. Frontend will not be served.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
