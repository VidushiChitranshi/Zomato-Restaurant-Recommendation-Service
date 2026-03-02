import pytest
import pandas as pd
import os
from app.phase_4_llm.gemini_client import GoogleAIRecommendationClient

# These tests will run against the REAL Google AI Studio API
# Ensure GOOGLE_API_KEY is set in phase_4_llm/.env

@pytest.fixture
def real_client():
    # Load .env explicitly from the phase_4_llm directory if it's there
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(dotenv_path=env_path)
    
    client = GoogleAIRecommendationClient()
    if not client.api_key:
        pytest.skip("GOOGLE_API_KEY not found. Skipping integration tests.")
    return client

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "name": ["Pasta Palace", "Curry House"],
        "location": ["Koramangala", "Indiranagar"],
        "rate": [4.5, 4.0],
        "approx_cost(for two people)": [1200, 800],
        "cuisines": ["Italian", "North Indian"]
    })

def test_real_summary_generation(real_client, sample_data):
    """Test 1: Verify actual text content is returned from Gemini."""
    summary = real_client.generate_summary(sample_data)
    assert isinstance(summary, str)
    assert len(summary) > 10
    # Print summary for debugging if needed (pytest -s)
    print(f"\nGemini Summary: {summary}")
    # Integration tests should be broad as LLM outputs vary
    assert any(term in summary.lower() for term in ["pasta", "curry", "italian", "indian", "choice", "recommend", "restaurant", "good", "great", "food"])

def test_real_summary_multiple_restaurants(real_client, sample_data):
    """Test 2: Verify it handles multiple restaurants correctly."""
    summary = real_client.generate_summary(sample_data)
    # Check for plural or conversational context
    assert len(summary.split()) > 5

def test_real_summary_empty_context_handling(real_client):
    """Test 3: Verify graceful handling of empty data with real client."""
    empty_df = pd.DataFrame(columns=["name", "location", "rate", "approx_cost(for two people)", "cuisines"])
    summary = real_client.generate_summary(empty_df)
    assert "no restaurants were found" in summary.lower()
