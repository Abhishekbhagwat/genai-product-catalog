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

import pandas as pd
from ..models import parse_row
from .config_utils import ConfigLoader
from ..chain_new import Command, Context


class CSVToRDMCommand(Command):
    def is_executable(self, context: Context) -> bool:
        return context.has_key('config') and context.has_key('csv_file_path')

    def execute(self, context: Context) -> None:
        config = context.get_value('config')
        csv_file_path = context.get_value('csv_file_path')

        df = pd.read_csv(csv_file_path) 

        products = []
        for index, row in df.iterrows():
            product = parse_row(row, pre_process=True)
            if product:
                products.append(product)

        context.add_value('rdm', products)