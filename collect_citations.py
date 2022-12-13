import json
import os
import pathlib

import requests

# see https://opencitations.net/index and https://opencitations.net/index/api/v1
# "references" for cited papers "citations" for citing papers
OPENCITATIONS_URL = "https://opencitations.net/index/coci/api/v1/citations/"
HEADERS = {}
if "OPENCITATIONS_ACCESS_TOKEN" in os.environ:
    HEADERS["authorization"] = os.environ["OPENCITATIONS_ACCESS_TOKEN"]
    print("Found opencitations access token; it will be added to HTTP headers")


all_dois = pathlib.Path("dfc_dois.txt").read_text("UTF-8").strip().split("\n")
all_citation_info = []
print("Downloading citation info from opencitations.net")
print("This may take a while...")
for doi in all_dois:
    print(f"fetching citation data for {doi}")
    citations = requests.get(f"{OPENCITATIONS_URL}{doi}", headers=HEADERS)
    citations.raise_for_status()
    all_citation_info.append(citations.json())

pathlib.Path("opencitations_data.json").write_text(
    json.dumps(all_citation_info), "UTF-8"
)
