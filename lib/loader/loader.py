#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  imitations under the License.

import pandas as pd
import model
from cmd_fetch import FetchImageCommand


def read_file():
    """
    Reads the import data file and produces a JSON file capable of being read by the retail data model.
    This allows for immediate import to any system that supports RDM.

    Since this is a bazel run program, the source is found from the runtime root.
    :return:
    """

    imageFetcher = FetchImageCommand()

    data = pd.read_csv(
        'third-party/flipkart/ecommerce-sample.csv',
        dtype=model.FILE_COLUMNS)

    data = data.drop_duplicates(subset=['product_name'])
    data = data.drop_duplicates(subset=['pid'])
    # data = data.dropna()

    f = open("flip_kart_product.json", "w")

    j = 0

    for i, row in data.iterrows():
        if j > 10:
            break
        j = j+1
        p = model.parse_row(row, True)
        if p is not None:
            print(p.product_name)

            for h in p.headers:
                for i in h.images:
                    imageFetcher.fetch_image(i)

            # if isinstance(p, model.Product) and p.headers[0].name != '':
            #     f.write(jsonpickle.encode(p, unpicklable=False) + "\n")

    f.close()


if __name__ == '__main__':
    read_file()
