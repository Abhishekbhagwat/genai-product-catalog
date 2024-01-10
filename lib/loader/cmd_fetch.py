
import requests
import configparser
from google.cloud import storage
from model import Image
storage_client = storage.Client()


class FetchImageCommand:
    bucket_name: str = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/loader.ini')
        FetchImageCommand.bucket_name = config['DEFAULT']['bucket_name']

    @staticmethod
    def fetch_image(image: Image) -> None:
        print(FetchImageCommand.bucket_name)
        print(image.url)