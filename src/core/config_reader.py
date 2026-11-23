import os
import yaml
from pathlib import Path


class ConfigReader:

    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "config" / "config.yaml"

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
                # Override browser settings using environment variables
        if isinstance(self.config, dict) and isinstance(self.config.get("browser"), dict):

            browser_env = os.getenv("BROWSER")

        if browser_env:
                self.config["browser"]["name"] = browser_env.lower()

        if os.getenv("CI", "").lower() == "true":
            self.config["browser"]["headless"] = True

        # Override Redis settings using environment variables
        if isinstance(self.config, dict) and isinstance(self.config.get("redis"), dict):

            redis_host = os.getenv("REDIS_HOST")
            redis_port = os.getenv("REDIS_PORT")
            redis_db = os.getenv("REDIS_DB")

            if redis_host:
                self.config["redis"]["host"] = redis_host

            if redis_port:
                self.config["redis"]["port"] = int(redis_port)

            if redis_db:
                self.config["redis"]["db"] = int(redis_db)

        self._validate_config()

    def _validate_config(self):
        required_settings = {
            "application": ["base_url"],
            "browser": ["name", "headless", "slow_mo"],
            "timeouts": ["default", "navigation"],
            "test": ["screenshot_on_failure"],
            "database": ["path"],
            "redis": ["host", "port", "db"]
        }

        if not isinstance(self.config, dict):
            raise ValueError("Configuration must contain a YAML mapping.")

        for section, keys in required_settings.items():
            if not isinstance(self.config.get(section), dict):
                raise ValueError(f"Missing or invalid section: {section}")

            for key in keys:
                if key not in self.config[section]:
                    raise ValueError(
                        f"Missing configuration setting: {section}.{key}"
                    )

        if not isinstance(self.config["application"]["base_url"], str) or not self.config["application"]["base_url"].strip():
            raise ValueError("Application base_url must be a non-empty string.")

        if self.config["browser"]["name"] not in ["chromium", "chrome", "edge"]:
            raise ValueError(
                "Unsupported browser. Choose chromium, chrome, or edge."
            )

        if not isinstance(self.config["browser"]["headless"], bool):
            raise ValueError("Browser headless must be true or false.")

        slow_mo = self.config["browser"]["slow_mo"]
        if isinstance(slow_mo, bool) or not isinstance(slow_mo, (int, float)) or slow_mo < 0:
            raise ValueError("Browser slow_mo must be a non-negative number.")

        for key in ["default", "navigation"]:
            timeout = self.config["timeouts"][key]
            if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
                raise ValueError(f"Timeout {key} must be a positive integer.")

        if not isinstance(self.config["test"]["screenshot_on_failure"], bool):
            raise ValueError("screenshot_on_failure must be true or false.")

        if not isinstance(self.config["database"]["path"], str) or not self.config["database"]["path"].strip():
            raise ValueError("Database path must be a non-empty string.")

        if not isinstance(self.config["redis"]["host"], str) or not self.config["redis"]["host"].strip():
            raise ValueError("Redis host must be a non-empty string.")

        if isinstance(self.config["redis"]["port"], bool) or not isinstance(self.config["redis"]["port"], int) or not 1 <= self.config["redis"]["port"] <= 65535:
            raise ValueError("Redis port must be an integer between 1 and 65535.")

        if isinstance(self.config["redis"]["db"], bool) or not isinstance(self.config["redis"]["db"], int) or self.config["redis"]["db"] < 0:
            raise ValueError("Redis database must be a non-negative integer.")

    def get(self, section, key):
        return self.config[section][key]
