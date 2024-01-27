import os
import tomllib

DATA: dict = None
configuration_file = os.environ.get("APPLIED_AI_CONF", "/usr/local/google/home/abhishekbhgwt/applied-ai/conf/app.toml")
with open(configuration_file, "rb") as f:
    DATA = tomllib.load(f)

class Config:
    DEFAULT_CONFIG = 'conf/app.ini'
    SECTION_DEFAULT = 'default'
    SECTION_PROJECT = 'project'
    SECTION_GCS = 'gcs'
    SECTION_MODELS = 'models'
    SECTION_VECTORS = 'vectors'
    SECTION_BIG_QUERY = 'big_query'
    SECTION_CATEGORY = 'category'
    SECTION_TEST = 'test'

    @staticmethod
    def value(section: str = SECTION_DEFAULT, key: str = None) -> str | list[any] | int | float | bool | None:
        if key is not None:
            return DATA[section][key]
        return None

