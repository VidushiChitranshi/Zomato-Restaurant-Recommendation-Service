import pytest
import pandas as pd
from app.phase_3_search.search_engine import RestaurantSearchEngine

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "name": ["Cafe Coffee Day", "Empire Restaurant", "Corner House", "Toscano"],
        "location": ["Koramangala 7th Block", "Indiranagar", "Koramangala 4th Block", "Whitefield"],
        "rate": [3.5, 4.2, 4.8, 4.5],
        "approx_cost(for two people)": [400, 800, 300, 1500],
        "cuisines": ["Cafe", "North Indian", "Ice Cream", "Italian"]
    })

def test_search_multiple_matches(sample_data):
    engine = RestaurantSearchEngine()
    # Search Koramangala, budget 500 -> CCD and Corner House
    results = engine.search(sample_data, "Koramangala", 500)
    assert len(results) == 2
    # Verify sorting (4.8 rating first)
    assert results.iloc[0]['name'] == "Corner House"

def test_search_partial_location_match(sample_data):
    engine = RestaurantSearchEngine()
    # 'Indira' should match 'Indiranagar'
    results = engine.search(sample_data, "Indira", 1000)
    assert len(results) == 1
    assert results.iloc[0]['name'] == "Empire Restaurant"

def test_search_no_results_location(sample_data):
    engine = RestaurantSearchEngine()
    # Non-existent location
    results = engine.search(sample_data, "Mars", 1000)
    assert len(results) == 0
    assert results.empty

def test_search_no_results_price(sample_data):
    engine = RestaurantSearchEngine()
    # Budget too low for any restaurant in Indiranagar
    results = engine.search(sample_data, "Indiranagar", 100)
    assert len(results) == 0

def test_search_boundary_price(sample_data):
    engine = RestaurantSearchEngine()
    # Budget exactly matching Imperio (800)
    results = engine.search(sample_data, "Indiranagar", 800)
    assert len(results) == 1
    assert results.iloc[0]['approx_cost(for two people)'] == 800

def test_search_case_insensitive_location(sample_data):
    engine = RestaurantSearchEngine()
    # Lowercase 'whitefield' should match 'Whitefield'
    results = engine.search(sample_data, "whitefield", 2000)
    assert len(results) == 1
    assert results.iloc[0]['name'] == "Toscano"

def test_search_respects_custom_limit():
    engine = RestaurantSearchEngine()
    # Create dummy data with 10 restaurants
    large_data = pd.DataFrame({
        "name": [f"Resto {i}" for i in range(10)],
        "location": ["Koramangala"] * 10,
        "rate": [4.0] * 10,
        "approx_cost(for two people)": [500] * 10,
        "cuisines": ["Any"] * 10
    })
    # Request 3 results
    results = engine.search(large_data, "Koramangala", 1000, limit=3)
    assert len(results) == 3

def test_search_default_limit_is_10():
    engine = RestaurantSearchEngine()
    # Create dummy data with 15 restaurants
    large_data = pd.DataFrame({
        "name": [f"Resto {i}" for i in range(15)],
        "location": ["Koramangala"] * 15,
        "rate": [4.0] * 15,
        "approx_cost(for two people)": [500] * 15,
        "cuisines": ["Any"] * 15
    })
    # default should be 10 as per our update
    results = engine.search(large_data, "Koramangala", 1000)
    assert len(results) == 10
