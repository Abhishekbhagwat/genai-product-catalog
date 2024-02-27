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

import tomllib
from typing import Dict, Any

from examples.loader.chain_new import Command, Context


class ConfigLoader(Command):
    def __init__(self, config_path: str):
        """
        Initialize the command with the path to the configuration file.
        :param config_path: Path to the .toml configuration file.
        """
        self.config_path = config_path

    def is_executable(self, context: Context) -> bool:
        # This command should always be executable since it initializes the context.
        # You might add additional logic here if there are preconditions for loading the config.
        return True

    def execute(self, context: Context) -> None:
        # Load and parse the TOML configuration file.
        with open(self.config_path, 'rb') as config_file:
            config_data = tomllib.load(config_file)
        
        # Iterate through the loaded configuration and add each value to the context.
        for section, values in config_data.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    # only keeping {key} instead of {section}.{key} as we assume that every variable name is unique
                    context.add_value(f"{key}", value)
                print(context.values)
            else:
                context.add_value(section, values)

# Example usage
config_loader = ConfigLoader('conf/app.toml')
context = Context()
config_loader.execute(context)