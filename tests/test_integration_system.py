import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app import main

# Integration tests for the full system flow
# We mock external dependencies like data loading and LLM API to ensure deterministic tests

@pytest.fixture
def mock_zomato_data():
    return pd.DataFrame({
        "name": ["Pasta Palace", "Curry King"],
        "location": ["Koramangala", "Indiranagar"],
        "rate": [4.5, 4.0],
        "approx_cost(for two people)": [1200.0, 800.0],
        "cuisines": ["Italian", "North Indian"]
    })

@patch('app.ZomatoLoader')
@patch('app.InputHandler')
@patch('app.GroqRecommendationClient')
def test_full_system_flow_happy_path(mock_llm_class, mock_input_class, mock_loader_class, mock_zomato_data, capsys):
    """Test 1: Full successful chain from input to display."""
    
    # 1. Mock Loader
    mock_loader = MagicMock()
    mock_loader.get_structured_data.return_value = mock_zomato_data
    mock_loader_class.return_value = mock_loader
    
    # 2. Mock Input
    mock_input = MagicMock()
    mock_input.get_user_preferences.return_value = {"location": "Koramangala", "max_price": 1500.0}
    mock_input_class.return_value = mock_input
    
    # 3. Mock LLM
    mock_llm = MagicMock()
    mock_llm.generate_summary.return_value = "AI says: Pasta Palace is the best Italian spot here."
    mock_llm_class.return_value = mock_llm
    
    # Run the system
    main()
    
    captured = capsys.readouterr().out
    assert "TOP RESTAURANT RECOMMENDATIONS" in captured
    assert "PASTA PALACE" in captured
    assert "AI says:" in captured
    assert "Rating: 4.5/5" in captured

@patch('app.ZomatoLoader')
@patch('app.InputHandler')
@patch('app.GroqRecommendationClient')
def test_system_no_results(mock_llm_class, mock_input_class, mock_loader_class, mock_zomato_data, capsys):
    """Test 2: System behavior when no restaurants match."""
    
    mock_loader = MagicMock()
    mock_loader.get_structured_data.return_value = mock_zomato_data
    mock_loader_class.return_value = mock_loader
    
    mock_input = MagicMock()
    mock_input.get_user_preferences.return_value = {"location": "Mars", "max_price": 10.0}
    mock_input_class.return_value = mock_input
    
    main()
    
    captured = capsys.readouterr().out
    assert "No restaurants matching your criteria were found" in captured
    # LLM should not be called
    mock_llm_class.return_value.generate_summary.assert_not_called()

@patch('app.ZomatoLoader')
@patch('app.InputHandler')
@patch('app.GroqRecommendationClient')
def test_system_llm_failure_resilience(mock_llm_class, mock_input_class, mock_loader_class, mock_zomato_data, capsys):
    """Test 3: System resilience when LLM fails but search works."""
    
    mock_loader = MagicMock()
    mock_loader.get_structured_data.return_value = mock_zomato_data
    mock_loader_class.return_value = mock_loader
    
    mock_input = MagicMock()
    mock_input.get_user_preferences.return_value = {"location": "Koramangala", "max_price": 1500.0}
    mock_input_class.return_value = mock_input
    
    # LLM returns error message
    mock_llm = MagicMock()
    mock_llm.generate_summary.return_value = "Failed to generate AI summary: API Error"
    mock_llm_class.return_value = mock_llm
    
    main()
    
    captured = capsys.readouterr().out
    assert "PASTA PALACE" in captured # Results still show
    assert "Failed to generate AI summary" in captured # Error message shows in AI section
