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

from google.cloud import bigquery

class BQEmbeddingLoaderCommand:
    @staticmethod
    def load_embeddings_to_bigquery(dataset_id: str, table_id: str, embeddings: str):
        client = bigquery.Client()
        table = client.dataset(dataset_id).table(table_id)
        rows_to_insert = [(embeddings,)]
        errors = client.insert_rows(table, rows_to_insert)
        if errors:
            print(f"Failed to load embeddings: {errors}")
            return False
        return True