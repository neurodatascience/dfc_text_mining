import json
import os
import pathlib

import pandas as pd
import requests

# see https://opencitations.net/index and https://opencitations.net/index/api/v1
# "references" for cited papers "citations" for citing papers
OPENCITATIONS_URL = "https://opencitations.net/index/coci/api/v1/citations/"
HEADERS = {}
if "OPENCITATIONS_ACCESS_TOKEN" in os.environ:
    HEADERS["authorization"] = os.environ["OPENCITATIONS_ACCESS_TOKEN"]
    print("Found opencitations access token; it will be added to HTTP headers")


all_dois = pathlib.Path("dfc_dois.txt").read_text("UTF-8").strip().split("\n")
all_responses_data = []
print("Downloading citation info from opencitations.net")
print("This may take a while...")
for doi in all_dois:
    print(f"fetching citation data for {doi}")
    citations = requests.get(f"{OPENCITATIONS_URL}{doi}", headers=HEADERS)
    citations.raise_for_status()
    all_responses_data.append(citations.json())

pathlib.Path("opencitations_rest_data.json").write_text(
    json.dumps(all_responses_data), "UTF-8"
)

citation_info = []
for resp_data in all_responses_data:
    for citation in resp_data:
        citation_info.append(
            {
                "citing_doi": citation["citing"],
                "cited_doi": citation["cited"],
            }
        )
pd.DataFrame(citation_info).sort_values(by=["cited_doi", "citing_doi"]).to_csv(
    "citations_doi.csv", index=False
)
