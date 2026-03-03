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

    def format_results(self, recommendations: pd.DataFrame, ai_data: Any) -> str:
        """
        Combines the restaurant list and AI summary into a pretty-printed string.
        `ai_data` can be a string (legacy) or a dict with 'overall_summary' and 'individual_summaries'.
        """
        if recommendations.empty:
            return "No restaurants matching your criteria were found. Please try a different location or price range."

        # Parse ai_data
        if isinstance(ai_data, dict):
            overall_summary = ai_data.get("overall_summary", "")
            individual_summaries = ai_data.get("individual_summaries", {})
        else:
            overall_summary = str(ai_data)
            individual_summaries = {}

        output = []
        output.append("\n" + "="*50)
        output.append("   TOP RESTAURANT RECOMMENDATIONS")
        output.append("="*50 + "\n")

        for i, (_, row) in enumerate(recommendations.iterrows(), 1):
            resto_name = row['name']
            output.append(f"{i}. {resto_name.upper()}")
            output.append(f"   Rating: {row['rate']}/5")
            output.append(f"   Cuisine: {row['cuisines']}")
            output.append(f"   Approx. Cost (2 people): Rs.{row['approx_cost(for two people)']}")
            output.append(f"   Location: {row['location']}")
            
            # Add individual insight if available
            insight = individual_summaries.get(resto_name)
            if insight:
                output.append(f"   ✨ Insight: {insight}")
                
            output.append("-" * 30)

        output.append("\n" + "*"*50)
        output.append("   AI CONTEXT & OVERALL SUMMARY")
        output.append("*"*50)
        output.append(overall_summary)
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
