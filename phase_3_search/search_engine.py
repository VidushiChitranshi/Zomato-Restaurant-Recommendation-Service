import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class RestaurantSearchEngine:
    """
    Phase 3: Search Logic
    Filters the Zomato dataset based on user preferences.
    """

    def search(self, df: pd.DataFrame, location: str, max_price: float, limit: int = 10) -> pd.DataFrame:
        """
        Filters the dataset by location and price.
        Returns a DataFrame of matching restaurants sorted by rating.
        """
        logger.info(f"Searching for restaurants in '{location}' with max price {max_price} (limit: {limit})...")

        # 1. Filter by Location (case-insensitive, contains)
        # We use .str.contains for flexibility (e.g., 'Koramangala' matches 'Koramangala 5th Block')
        mask_location = df['location'].str.contains(location, case=False, na=False)

        # 2. Filter by Price (<= max_price)
        mask_price = df['approx_cost(for two people)'] <= max_price

        # Combine masks
        filtered_df = df[mask_location & mask_price].copy()

        # 3. Sort by rate (highest first)
        if not filtered_df.empty:
            filtered_df = filtered_df.sort_values(by='rate', ascending=False)
            filtered_df = filtered_df.head(limit)
            logger.info(f"Top {len(filtered_df)} matches selected.")
        else:
            logger.warning("No matches found for the given criteria.")

        return filtered_df

if __name__ == "__main__":
    # Quick sanity check with dummy data
    engine = RestaurantSearchEngine()
    dummy_data = pd.DataFrame({
        "name": ["A", "B", "C"],
        "location": ["Koramangala", "Indiranagar", "Koramangala"],
        "rate": [4.5, 3.8, 4.0],
        "approx_cost(for two people)": [800, 1200, 500],
        "cuisines": ["Chinese", "Italian", "Indian"]
    })
    
    results = engine.search(dummy_data, "Koramangala", 1000)
    print("Search Results (Koramangala, <1000):")
    print(results)
