import tomllib as toml

class ConfigLoader:
    """Loads configuration from a TOML file"""

    CONFIG_FILE_PATH = "conf/app.toml"

    def __init__(self):
        self._config = None  # Store the loaded config

    def load_config(self) -> dict:
        """Loads the configuration from the TOML file"""
        with open(self.CONFIG_FILE_PATH, 'r') as f:
            self._config = toml.load(f)
        return self._config

    def get_config(self) -> dict:
        """Retrieves the loaded configuration"""
        if self._config is None:
            self.load_config() 
        return self._config
