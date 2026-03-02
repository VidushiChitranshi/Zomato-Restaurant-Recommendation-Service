import pytest
from unittest.mock import patch
from app.phase_2_input.input_handler import InputHandler

def test_get_location_valid():
    handler = InputHandler(valid_locations=["Indiranagar"])
    with patch('builtins.input', return_value="Indiranagar"):
        assert handler.get_location() == "Indiranagar"

def test_get_location_empty_then_valid():
    handler = InputHandler(valid_locations=["Koramangala"])
    # First call empty, second call valid
    with patch('builtins.input', side_effect=["", "Koramangala"]):
        assert handler.get_location() == "Koramangala"

def test_get_location_invalid_then_valid():
    handler = InputHandler(valid_locations=["Koramangala"])
    # First call invalid location, second call valid
    with patch('builtins.input', side_effect=["Mars", "Koramangala"]):
        assert handler.get_location() == "Koramangala"

def test_get_max_price_valid():
    handler = InputHandler()
    with patch('builtins.input', return_value="500"):
        assert handler.get_max_price() == 500.0

def test_get_max_price_invalid_then_valid():
    handler = InputHandler()
    # Sequence: invalid string, negative number, too high (>10000), then valid
    with patch('builtins.input', side_effect=["abc", "-10", "15000", "1200"]):
        assert handler.get_max_price() == 1200.0

def test_get_user_preferences_integration():
    handler = InputHandler(valid_locations=["Jayanagar"])
    with patch('builtins.input', side_effect=["Jayanagar", "1500"]):
        prefs = handler.get_user_preferences()
        assert prefs == {"location": "Jayanagar", "max_price": 1500.0}

def test_get_location_whitespace():
    handler = InputHandler(valid_locations=["Whitefield"])
    with patch('builtins.input', side_effect=["   ", "Whitefield"]):
        assert handler.get_location() == "Whitefield"

def test_get_max_price_zero():
    handler = InputHandler()
    # Zero should be rejected, then 100 accepted
    with patch('builtins.input', side_effect=["0", "100"]):
        assert handler.get_max_price() == 100.0

def test_get_max_price_very_large():
    handler = InputHandler()
    # Sequence: too high (>10000), then valid
    with patch('builtins.input', side_effect=["999999999", "5000"]):
        assert handler.get_max_price() == 5000.0

def test_get_location_unicode():
    handler = InputHandler(valid_locations=["Béngaluru"])
    with patch('builtins.input', return_value="Béngaluru"):
        assert handler.get_location() == "Béngaluru"

def test_get_max_price_decimal():
    handler = InputHandler()
    with patch('builtins.input', return_value="450.50"):
        assert handler.get_max_price() == 450.5

def test_get_location_quit():
    handler = InputHandler(valid_locations=["Indiranagar"])
    with patch('builtins.input', return_value="q"):
        assert handler.get_location() is None
