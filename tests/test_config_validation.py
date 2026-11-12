
import pytest
from src.core.config_reader import ConfigReader


def test_invalid_browser_configuration():
    config = ConfigReader()

    # Intentionally provide an unsupported browser name
    config.config["browser"]["name"] = "invalid_browser"

    # Verify that configuration validation rejects it
    with pytest.raises(ValueError, match="Unsupported browser"):
        config._validate_config()
