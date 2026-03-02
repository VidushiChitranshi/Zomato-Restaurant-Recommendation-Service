import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class RestaurantFormatter:
    """
    Phase 5: Output Presentation
    Formats the final restaurant list and AI narrative for display.
    """

    def format_results(self, recommendations: pd.DataFrame, ai_summary: str) -> str:
        """
        Combines the restaurant list and AI summary into a pretty-printed string.
        """
        if recommendations.empty:
            return "No restaurants matching your criteria were found. Please try a different location or price range."

        output = []
        output.append("\n" + "="*50)
        output.append("   TOP RESTAURANT RECOMMENDATIONS")
        output.append("="*50 + "\n")

        for i, (_, row) in enumerate(recommendations.iterrows(), 1):
            output.append(f"{i}. {row['name'].upper()}")
            output.append(f"   Rating: {row['rate']}/5")
            output.append(f"   Cuisine: {row['cuisines']}")
            output.append(f"   Approx. Cost (2 people): Rs.{row['approx_cost(for two people)']}")
            output.append(f"   Location: {row['location']}")
            output.append("-" * 30)

        output.append("\n" + "*"*50)
        output.append("   AI CONTEXT & SUMMARY")
        output.append("*"*50)
        output.append(ai_summary)
        output.append("*"*50 + "\n")

        return "\n".join(output)

if __name__ == "__main__":
    # Quick sanity check
    formatter = RestaurantFormatter()
    dummy_df = pd.DataFrame({
        "name": ["Empire Restaurant", "Truffles"],
        "location": ["Indiranagar", "Koramangala"],
        "rate": [4.2, 4.5],
        "approx_cost(for two people)": [800.0, 1200.0],
        "cuisines": ["North Indian", "Burgers"]
    })
    dummy_summary = "Empire is a classic for Indian food, while Truffles is famous for its burgers."
    print(formatter.format_results(dummy_df, dummy_summary))
