import io
import os
import re

import setuptools  # type: ignore

package_root = os.path.abspath(os.path.dirname(__file__))
name = "google-cloud-ml-applied"

description = "Google Cloud ML Applied Client Library"

version = None

with open(os.path.join(package_root, "google/cloud/ml/applied/gapic_version.py")) as fp:
    version_candidates = re.findall(r"(?<=\")\d+.\d+.\d+(?=\")", fp.read())
    assert len(version_candidates) == 1
    version = version_candidates[0]

if version[0] == "0":
    release_status = "Development Status :: 4 - Beta"
else:
    release_status = "Development Status :: 5 - Production/Stable"


readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

url = "https://github.com/"

packages = [
  package
  for package in setuptools.find_namespace_packages()
  if package.startswith("google")
]

dependencies = [
  "requests"
  "scipy",
  "numpy",
  "mediapipe",
  "pandas",
  "en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.4.0/en_core_web_sm-3.4.0-py3-none-any.whl"
  "spacy",
  "spacy-cleaner",
  "json-pickle",
  "google-api-python-client",
  "google-cloud-aiplatform>=1.39.0",
  "google-cloud-storage",
  "google-cloud-bigquery",
  "gcloud",
  "grpclib",
  "grpcio",
  "fastapi>=0.108.0",
  "uvicorn",
]

setuptools.setup(
  name=name,
  version=version,
  description=description,
  long_description=readme,
  author="Google LLC",
  author_email="googleapis-packages@google.com",
  license="Apache 2.0",
  url=url,
  classifiers=[
    release_status,
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Operating System :: OS Independent",
    "Topic :: Internet",
  ],
  platforms="Posix; MacOS X; Windows",
  packages=packages,
  python_requires=">=3.7",
  install_requires=dependencies,
  include_package_data=True,
  zip_safe=False,
)