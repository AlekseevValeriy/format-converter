import pytest


def test_mode():
    pytest.main(["-vv", "--tb=long", "../tests"])
