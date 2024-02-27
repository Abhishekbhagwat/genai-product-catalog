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