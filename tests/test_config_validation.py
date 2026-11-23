
import pytest
from src.core.config_reader import ConfigReader
import pytest
from src.core.config_reader import ConfigReader


def test_invalid_browser_configuration():
    config = ConfigReader()

    # Intentionally provide an unsupported browser name
    config.config["browser"]["name"] = "invalid_browser"

    # Verify that configuration validation rejects it
    with pytest.raises(ValueError, match="Unsupported browser"):
        config._validate_config()

def test_invalid_browser_configuration():
    config = ConfigReader()

    # Intentionally provide an unsupported browser name
    config.config["browser"]["name"] = "invalid_browser"

    # Verify that configuration validation rejects it
    with pytest.raises(ValueError, match="Unsupported browser"):
        config._validate_config()


def test_invalid_redis_host():
    config = ConfigReader()

    config.config["redis"]["host"] = ""

    with pytest.raises(ValueError, match="Redis host"):
        config._validate_config()


def test_invalid_redis_port():
    config = ConfigReader()

    config.config["redis"]["port"] = 70000

    with pytest.raises(ValueError, match="Redis port"):
        config._validate_config()


def test_invalid_redis_database():
    config = ConfigReader()

    config.config["redis"]["db"] = -1

    with pytest.raises(ValueError, match="Redis database"):
        config._validate_config()


def test_valid_redis_configuration():
    config = ConfigReader()

    config._validate_config()
