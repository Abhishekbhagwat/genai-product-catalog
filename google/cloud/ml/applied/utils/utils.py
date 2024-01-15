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
import configparser
import vertexai
import vertexai.preview

from functools import cache
from typing import Any
from google.cloud import aiplatform_v1
from google.cloud import bigquery
from vertexai.preview.generative_models import (GenerativeModel)

DEFAULT_CONFIG = 'conf/app.ini'
SECTION_DEFAULT = 'default'
SECTION_PROJECT = 'project'
SECTION_GCS = 'gcs'
SECTION_MODELS = 'models'
SECTION_VECTORS = 'vectors'
SECTION_BIG_QUERY = 'big_query'
SECTION_CATEGORY = 'category'
SECTION_TEST = 'test'

config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG)


def str_value(section: str, key: str) -> str:
    return config[section][key]


def int_value(section: str = SECTION_DEFAULT, key: str = '') -> int:
    return int(config[section][key])


def bool_value(section: str = SECTION_DEFAULT, key: str = '') -> bool:
    str_val = str_value(section, key)
    return str_val is not None and str_val.lower() == 'true'


def list_value(section: str = SECTION_DEFAULT, key: str = '') -> list:
    str_val = str_value(section, key)
    out = []
    if str is not None:
        out.extend(str_val.replace('[', '').replace(']', '').split('.'))

    return out


@cache
def get_bq_client(project=str_value(SECTION_PROJECT, 'id')):
    return bigquery.Client(project)


@cache
def get_llm():
    vertexai.init(project=str_value(SECTION_PROJECT, 'id'),
                  location=str_value(SECTION_PROJECT, 'location'))

    return (vertexai.
            language_models.
            TextGenerationModel.
            from_pretrained(str_value(SECTION_MODELS, 'llm')))


@cache
def get_gemini_pro_vision() -> Any:
    multimodal_model = (
        GenerativeModel(
            str_value(SECTION_MODELS, 'gemini')))

    return multimodal_model


@cache
def get_vector_search_index_client():
    index_client = aiplatform_v1.IndexServiceClient(
        client_options=dict(api_endpoint=str_value(SECTION_PROJECT, 'endpoint')))

    return index_client



