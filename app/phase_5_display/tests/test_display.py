import pytest
import pandas as pd
from app.phase_5_display.formatter import RestaurantFormatter

@pytest.fixture
def sample_recommendations():
    return pd.DataFrame({
        "name": ["Pasta Palace"],
        "location": ["Koramangala"],
        "rate": [4.5],
        "approx_cost(for two people)": [1200.0],
        "cuisines": ["Italian"]
    })

def test_format_results_success(sample_recommendations):
    formatter = RestaurantFormatter()
    summary = "A great choice for lovers of authentic Italian pasta."
    result = formatter.format_results(sample_recommendations, summary)
    
    assert "PASTA PALACE" in result
    assert "Rating: 4.5/5" in result
    assert "₹1200.0" in result
    assert "AI CONTEXT & SUMMARY" in result
    assert summary in result

def test_format_results_empty():
    formatter = RestaurantFormatter()
    result = formatter.format_results(pd.DataFrame(), "No summary")
    assert "No restaurants matching your criteria" in result
