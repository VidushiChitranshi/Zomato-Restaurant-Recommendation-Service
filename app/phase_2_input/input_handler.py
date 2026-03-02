import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class InputHandler:
    """
    Phase 2: User Input Handling
    Captures and validates location and price preferences from the CLI.
    """
    def __init__(self, valid_locations: list = None):
        self.valid_locations = sorted(valid_locations) if valid_locations is not None else []

    def _display_available_locations(self):
        """
        Prints all valid locations in a formatted column layout.
        """
        if not self.valid_locations:
            return

        print("\nPlease select your location from the following options:")
        print("-" * 60)
        
        # Display in 3 columns for better readability
        cols = 3
        rows = (len(self.valid_locations) + cols - 1) // cols
        
        for r in range(rows):
            line = ""
            for c in range(cols):
                idx = r + c * rows
                if idx < len(self.valid_locations):
                    line += f"{self.valid_locations[idx]:<20}"
            print(line)
        print("-" * 60)

    def get_location(self) -> str:
        """
        Prompts the user for a location and validates it against the dataset.
        """
        self._display_available_locations()
        
        while True:
            location = input(
                "\nEnter preferred restaurant location (e.g., Koramangala) or 'q' to quit: "
            ).strip()

            if location.lower() in ['q', 'quit']:
                return None

            if not location:
                print("Error: Location cannot be empty. Please try again.")
                continue

            # Case-insensitive check against valid_locations if list is provided
            if self.valid_locations:
                valid_loc_lower = [loc.lower() for loc in self.valid_locations]
                if location.lower() not in valid_loc_lower:
                    print("\nThe input value does not match with the database. Please choose value from the database only.")
                    continue

            return location

    def get_max_price(self) -> float:
        """
        Prompts the user for a maximum price and validates it.
        """
        while True:
            price_str = input("Enter maximum price for two people (e.g., 1000): ").strip()
            if not price_str:
                print("Error: Price cannot be empty. Please try again.")
                continue
            try:
                price = float(price_str)
                if price <= 0:
                    print("Error: Price must be a positive number. Please try again.")
                    continue
                if price > 10000:
                    print("Error: Price cannot exceed 10,000. Please try again.")
                    continue
                return price
            except ValueError:
                print("Error: Invalid price format. Please enter a numeric value.")

    def get_limit(self) -> int:
        """
        Prompts the user for the number of results to display.
        """
        while True:
            limit_str = input("Enter number of results to display (3-20, default 10): ").strip()
            if not limit_str:
                return 10
            try:
                limit = int(limit_str)
                if 3 <= limit <= 20:
                    return limit
                print("Error: Limit must be between 3 and 20. Please try again.")
            except ValueError:
                print("Error: Invalid limit format. Please enter a numeric value.")

    def get_user_preferences(self) -> dict:
        """
        Orchestration method for Phase 2.
        """
        logger.info("Starting user input collection...")
        location = self.get_location()
        if location is None:
            return {"location": None, "max_price": None, "limit": None}
            
        max_price = self.get_max_price()
        limit = self.get_limit()
        
        return {
            "location": location,
            "max_price": max_price,
            "limit": limit
        }

if __name__ == "__main__":
    # Quick sanity check
    from app.phase_1_data.dataset_loader import ZomatoLoader
    
    try:
        loader = ZomatoLoader()
        df = loader.get_structured_data()
        valid_locations = df["location"].dropna().unique().tolist()
        
        handler = InputHandler(valid_locations)
        prefs = handler.get_user_preferences()
        print(f"User Preferences: {prefs}")
    except KeyboardInterrupt:
        print("\nInput cancelled by user.")
    except Exception as e:
        print(f"Error during manual run: {e}")
