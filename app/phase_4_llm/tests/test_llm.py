import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from app.phase_4_llm.gemini_client import GoogleAIRecommendationClient

@pytest.fixture
def sample_recommendations():
    return pd.DataFrame({
        "name": ["Empire Restaurant", "Corner House"],
        "location": ["Indiranagar", "Koramangala"],
        "rate": [4.2, 4.8],
        "approx_cost(for two people)": [800.0, 300.0],
        "cuisines": ["North Indian", "Ice Cream"]
    })

def test_build_prompt(sample_recommendations):
    client = GoogleAIRecommendationClient(api_key="fake_key")
    prompt = client._build_prompt(sample_recommendations)
    assert "Empire Restaurant" in prompt
    assert "Indiranagar" in prompt
    assert "4.2" in prompt
    assert "Corner House" in prompt

def test_generate_summary_no_client():
    # Test behavior when API key is missing
    with patch('os.getenv', return_value=None):
        client = GoogleAIRecommendationClient()
        assert "AI summary unavailable" in client.generate_summary(pd.DataFrame())

def test_generate_summary_empty_df():
    client = GoogleAIRecommendationClient(api_key="fake_key")
    summary = client.generate_summary(pd.DataFrame())
    assert "No restaurants were found" in summary

@patch('google.genai.Client')
def test_generate_summary_success(mock_client_class, sample_recommendations):
    # Mock the Gemini client and its response
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = "These are great restaurants because they offer diverse cuisines and have high ratings."
    mock_client.models.generate_content.return_value = mock_response
    
    client = GoogleAIRecommendationClient(api_key="fake_key")
    summary = client.generate_summary(sample_recommendations)
    
    assert "These are great restaurants" in summary
    mock_client.models.generate_content.assert_called_once()

@patch('google.genai.Client')
def test_generate_summary_error(mock_client_class, sample_recommendations):
    # Mock the Gemini client to raise an exception
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client
    mock_client.models.generate_content.side_effect = Exception("API connection failure")
    
    client = GoogleAIRecommendationClient(api_key="fake_key")
    summary = client.generate_summary(sample_recommendations)
    
    assert "Failed to generate AI summary" in summary
    assert "API connection failure" in summary
