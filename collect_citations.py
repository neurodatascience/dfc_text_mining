import os
import pathlib

import requests

# see https://opencitations.net/index and https://opencitations.net/index/api/v1
# "references" for cited papers "citations" for citing papers
OPENCITATIONS_URL = "https://opencitations.net/index/coci/api/v1/citations/"
HEADERS = {}
if "OPENCITATIONS_ACCESS_TOKEN" in os.environ:
    HEADERS["authorization"] = os.environ["OPENCITATIONS_ACCESS_TOKEN"]


all_dois = pathlib.Path("dfc_dois.txt").read_text("UTF-8").strip().split("\n")
citations = requests.get(f"{OPENCITATIONS_URL}{all_dois[0]}", headers=HEADERS)
print(citations.json())
