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

import concurrent.futures

import pandas as pd

import model
from commands.cmd_fetch import FetchImageCommand


def read_file():
    """
    Reads the import data file and produces a JSON file capable of being read by the retail data model.
    This allows for immediate import to any system that supports RDM.

    Since this is a bazel run program, the source is found from the runtime root.
    :return:
    """

    image_fetcher = FetchImageCommand()

    data = pd.read_csv(
        '/usr/local/google/home/abhishekbhgwt/applied-ai/third_party/flipkart/ecommerce-sample.csv',
        dtype=model.FILE_COLUMNS)

    data = data.drop_duplicates(subset=['product_name'])
    data = data.drop_duplicates(subset=['pid'])
    # data = data.dropna()

    f = open("flip_kart_product.json", "w")

    j = 0

    all_futures = []
    total_images = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for i, row in data.iterrows():
            if j > 10:
                break
            j = j + 1
            p = model.parse_row(row, True)
            if p is not None:
                for h in p.headers:
                    print(h.name)
                    total_images += len(h.images)
                    all_futures.extend({executor.submit(image_fetcher.fetch_image, i): i for i in h.images})
    f.close()

    for future in concurrent.futures.as_completed(all_futures):
        try:
            r = future.result()
            print(r)
        except Exception as e:
            print(e)

    print("Total Images: %d" % total_images)


if __name__ == '__main__':
    read_file()
