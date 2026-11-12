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

        self._validate_config()

    def _validate_config(self):
        required_settings = {
            "application": ["base_url"],
            "browser": ["name", "headless", "slow_mo"],
            "timeouts": ["default", "navigation"],
            "test": ["screenshot_on_failure"]
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

    def get(self, section, key):
        return self.config[section][key]
