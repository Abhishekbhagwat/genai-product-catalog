import configparser

from model import Image


class FetchImageCommand:
    bucket_name: str = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf/app.ini')
        FetchImageCommand.bucket_name = "rdm-demo-images2"

    @staticmethod
    def fetch_image(image: Image) -> bool:
        print(FetchImageCommand.bucket_name)
        print(image.origin_url)
        print(image.url)

        return True
