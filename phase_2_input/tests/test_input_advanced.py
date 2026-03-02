import pytest
from unittest.mock import patch
from phase_2_input.input_handler import InputHandler

def test_get_location_extremely_long():
    handler = InputHandler()
    long_location = "A" * 1000
    with patch('builtins.input', return_value=long_location):
        assert handler.get_location() == long_location

def test_get_max_price_very_large():
    handler = InputHandler()
    # Sequence: too high (>10000), then valid
    with patch('builtins.input', side_effect=["999999999", "10000"]):
        assert handler.get_max_price() == 10000.0

def test_get_max_price_leading_plus():
    handler = InputHandler()
    with patch('builtins.input', return_value="+500"):
        assert handler.get_max_price() == 500.0

def test_get_max_price_whitespace_padding():
    handler = InputHandler()
    with patch('builtins.input', return_value="  750.0  "):
        assert handler.get_max_price() == 750.0

def test_get_location_with_numbers():
    handler = InputHandler()
    # A location string that is purely numeric should still be accepted as a string
    with patch('builtins.input', return_value="560001"):
        assert handler.get_location() == "560001"

def test_get_location_emoji():
    handler = InputHandler()
    with patch('builtins.input', return_value="🍕 City"):
        assert handler.get_location() == "🍕 City"

def test_get_max_price_invalid_format_retries():
    handler = InputHandler()
    # Test multiple failures (hex, empty, invalid) then valid
    with patch('builtins.input', side_effect=["0x123", "", "!!!", "600"]):
        assert handler.get_max_price() == 600.0
