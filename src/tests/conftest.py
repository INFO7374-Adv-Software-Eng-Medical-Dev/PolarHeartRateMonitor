import pytest

@pytest.fixture
def mock_discover():
    return ["AA:BB:CC:DD:EE:FF: Device 1", "11:22:33:44:55:66: Device 2", "FF:EE:DD:CC:BB:AA: None"]