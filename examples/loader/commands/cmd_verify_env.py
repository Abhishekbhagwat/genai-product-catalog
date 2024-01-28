import configparser
import os

class VerifyEnvironmentCommand:
    bucket_name: str = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/app.toml')
        VerifyEnvironmentCommand.bucket_name = config['default']['bucket_name']

    @staticmethod
    def verify_environment() -> bool:
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            print("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set.")
            return False
        print("Environment is properly set.")
        return True