import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.phase_1_data.dataset_loader import ZomatoLoader

@pytest.fixture
def mock_raw_data():
    return pd.DataFrame({
        "name": ["Resto A", "Resto B", "Resto C", "Resto A"], # Duplicate name for A
        "location": ["Koramangala", "Indiranagar", "Koramangala", "Koramangala"],
        "rate": ["4.1/5", "3.8/5", "NEW", "4.1/5"],
        "approx_cost(for two people)": ["800", "1,200", None, "800"],
        "cuisines": ["North Indian", "South Indian", "Cafe", "North Indian"],
        "unused_col": [1, 2, 3, 1]
    })

def test_clean_data_duplicates(mock_raw_data):
    loader = ZomatoLoader()
    clean_df = loader.clean_data(mock_raw_data)
    # 4 rows, 1 is a duplicate across ALL columns (mostly)
    # actually Resto A is identical in all columns including rate and cost
    assert len(clean_df) == 3

def test_clean_rate_numeric(mock_raw_data):
    loader = ZomatoLoader()
    clean_df = loader.clean_data(mock_raw_data)
    # "4.1/5" -> 4.1, "NEW" -> None
    assert clean_df.iloc[0]['rate'] == 4.1
    assert pd.isna(clean_df.iloc[2]['rate'])

def test_clean_cost_numeric(mock_raw_data):
    loader = ZomatoLoader()
    clean_df = loader.clean_data(mock_raw_data)
    # "1,200" -> 1200.0
    # Search for Resto B which was index 1
    resto_b = clean_df[clean_df['name'] == "Resto B"].iloc[0]
    assert resto_b['approx_cost(for two people)'] == 1200.0

def test_schema_validation():
    loader = ZomatoLoader()
    invalid_df = pd.DataFrame({"name": ["Test"]})
    with pytest.raises(ValueError, match="Missing required columns"):
        loader.clean_data(invalid_df)

def test_null_handling_essential():
    loader = ZomatoLoader()
    df_with_nulls = pd.DataFrame({
        "name": [None, "Valid"],
        "location": ["Loc", None],
        "rate": ["4/5", "4/5"],
        "approx_cost(for two people)": ["100", "100"],
        "cuisines": ["A", "B"]
    })
    clean_df = loader.clean_data(df_with_nulls)
    # Both rows should be dropped because name or location is null
    assert len(clean_df) == 0

@patch("app.phase_1_data.dataset_loader.load_dataset")
def test_load_data_success(mock_load):
    # Mocking the datasets.load_dataset return value
    mock_dataset = MagicMock()
    mock_dataset.to_pandas.return_value = pd.DataFrame({"name": [" Mock Resto "]})
    mock_load.return_value = mock_dataset
    
    loader = ZomatoLoader()
    df = loader.load_data()
    assert len(df) == 1
    assert df.iloc[0]['name'] == " Mock Resto "

def test_clean_large_cost():
    loader = ZomatoLoader()
    df = pd.DataFrame({
        "name": ["Fancy Place"],
        "location": ["CBD"],
        "rate": ["4.9/5"],
        "approx_cost(for two people)": ["10,00,000"],
        "cuisines": ["Fine Dine"]
    })
    clean_df = loader.clean_data(df)
    assert clean_df.iloc[0]['approx_cost(for two people)'] == 1000000.0

def test_handle_decimal_rate():
    loader = ZomatoLoader()
    df = pd.DataFrame({
        "name": ["Cafe"],
        "location": ["Indiranagar"],
        "rate": ["3.14/5"],
        "approx_cost(for two people)": ["500"],
        "cuisines": ["Coffee"]
    })
    clean_df = loader.clean_data(df)
    assert clean_df.iloc[0]['rate'] == 3.14

def test_clean_invalid_cost_string():
    loader = ZomatoLoader()
    df = pd.DataFrame({
        "name": ["Free Food"],
        "location": ["Street"],
        "rate": ["5/5"],
        "approx_cost(for two people)": ["Price on request"],
        "cuisines": ["None"]
    })
    clean_df = loader.clean_data(df)
    assert pd.isna(clean_df.iloc[0]['approx_cost(for two people)'])

def test_empty_dataframe_handling():
    loader = ZomatoLoader()
    empty_df = pd.DataFrame(columns=loader.REQUIRED_COLUMNS)
    clean_df = loader.clean_data(empty_df)
    assert len(clean_df) == 0

@patch.object(ZomatoLoader, 'load_data')
def test_get_structured_data_orchestration(mock_load):
    mock_df = pd.DataFrame({
        "name": ["A"], "location": ["L"], "rate": ["4/5"], 
        "approx_cost(for two people)": ["100"], "cuisines": ["C"], "extra": ["X"]
    })
    mock_load.return_value = mock_df
    loader = ZomatoLoader()
    result = loader.get_structured_data()
    assert list(result.columns) == loader.REQUIRED_COLUMNS
    assert len(result) == 1
