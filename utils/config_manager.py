"""Configuration manager for handling YAML config files and environment variables."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration from YAML files and environment variables."""
    def __init__(self, config_path: str = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to the configuration file. Defaults to config/config.yml
        """
        # Load environment variables
        load_dotenv()

        # Set default config path
        if config_path is None:
            config_path = Path(
                __file__).parent.parent / "config" / "config.yml"

        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        # Replace environment variables
        return self._replace_env_vars(config)

    def _replace_env_vars(self, config: Any) -> Any:
        """Recursively replace environment variables in configuration.
        
        Args:
            config: Configuration object (dict, list, or value)
            
        Returns:
            Configuration with environment variables replaced
        """
        if isinstance(config, dict):
            return {
                key: self._replace_env_vars(value)
                for key, value in config.items()
            }
        elif isinstance(config, list):
            return [self._replace_env_vars(item) for item in config]
        elif isinstance(
                config,
                str) and config.startswith('${') and config.endswith('}'):
            # Extract environment variable name and default value
            env_expr = config[2:-1]
            if ':' in env_expr:
                env_name, default_value = env_expr.split(':', 1)
                return os.getenv(env_name, default_value)
            else:
                value = os.getenv(env_expr)
                if value is None:
                    raise ValueError(
                        f"Environment variable not found: {env_expr}")
                return value
        else:
            return config

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by key path.
        
        Args:
            key_path: Dot-separated path to the configuration key (e.g., 'api.base_url')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration."""
        return self.get('api', {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get('logging', {})

    def get_test_data(self) -> Dict[str, Any]:
        """Get test data configuration."""
        return self.get('test_data', {})

    def reload(self):
        """Reload configuration from file."""
        self._config = self._load_config()


# Global configuration instance
config = ConfigManager()
