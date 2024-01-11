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


"""Functions common to several modules."""
from functools import cache
from typing import Any

import config
import vertexai
import vertexai.preview
from google.cloud import aiplatform_v1
from google.cloud import bigquery
from vertexai.preview.generative_models import (GenerativeModel)


@cache
def get_bq_client(project=config.PROJECT):
    return bigquery.Client(project)


@cache
def get_llm(project=config.PROJECT, location=config.LOCATION):
    vertexai.init(project=config.PROJECT, location=config.LOCATION)
    return vertexai.language_models.TextGenerationModel.from_pretrained(
        "text-bison")


@cache
def get_gemini_pro_vision() -> Any:
    multimodal_model = GenerativeModel("gemini-pro-vision")
    return multimodal_model


@cache
def get_vector_search_index_client():
    index_client = aiplatform_v1.IndexServiceClient(
        client_options=dict(api_endpoint=config.ENDPOINT))
    return index_client
