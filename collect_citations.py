import json
import os
import pathlib

import requests

# see https://opencitations.net/index and https://opencitations.net/index/api/v1
OPENCITATIONS_URL = "https://w3id.org/oc/index/api/v1/metadata/"
HEADERS = {}
if "OPENCITATIONS_ACCESS_TOKEN" in os.environ:
    HEADERS["authorization"] = os.environ["OPENCITATIONS_ACCESS_TOKEN"]


all_dois = pathlib.Path("dfc_dois.txt").read_text("UTF-8").strip().split("\n")
citations = requests.get(
    f"{OPENCITATIONS_URL}{'__'.join(all_dois)}", headers=HEADERS
)
pathlib.Path("opencitations_data.json").write_text(
    json.dumps(citations.json()), encoding="UTF-8"
)
