# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
