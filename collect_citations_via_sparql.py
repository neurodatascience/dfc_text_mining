import json
import os
import pathlib
import string

import pandas as pd
import requests

OPENCITATIONS_URL = "https://opencitations.net/index/sparql"
HEADERS = {
    "Content-Type": "application/sparql-query",
    "Accept": "application/json",
}
if "OPENCITATIONS_ACCESS_TOKEN" in os.environ:
    HEADERS["authorization"] = os.environ["OPENCITATIONS_ACCESS_TOKEN"]
    print("Found opencitations access token; it will be added to HTTP headers")

QUERY_TEMPLATE = string.Template(
    """
PREFIX cito:<http://purl.org/spar/cito/>

SELECT DISTINCT ?citing_entity ?cited_entity  WHERE {
GRAPH <https://w3id.org/oc/index/coci/> {
${SELECT_BLOCKS}
}
}
"""
)

SELECT_TEMPLATE = string.Template(
    """{
?citation a cito:Citation;
cito:hasCitingEntity ?citing_entity ;
cito:hasCitedEntity ?cited_entity;
cito:hasCitedEntity <http://dx.doi.org/${DOI}>;
}"""
)

all_dois = pathlib.Path("dfc_dois.txt").read_text("UTF-8").strip().split("\n")

select_blocks = "\nUNION\n".join(
    SELECT_TEMPLATE.substitute({"DOI": doi}) for doi in all_dois
)
query = QUERY_TEMPLATE.substitute({"SELECT_BLOCKS": select_blocks})
print(f"Running query against SPARQL endpoint:\n{query}")
print("This may take a while...")
resp = requests.post(
    OPENCITATIONS_URL, data=query.encode("UTF-8"), headers=HEADERS
)
print(f"Received response {resp.status_code}")
resp.raise_for_status()
resp_data = resp.json()
pathlib.Path("opencitations_sparql_data.json").write_text(
    json.dumps(resp_data), encoding="UTF-8"
)

citation_info = []
for result in resp_data["results"]["bindings"]:
    citation_info.append(
        {
            "citing_doi": result["citing_entity"]["value"].lstrip(
                "http://dx.doi.org/"
            ),
            "cited_doi": result["cited_entity"]["value"].lstrip(
                "http://dx.doi.org"
            ),
        }
    )
pd.DataFrame(citation_info).sort_values(by=["cited_doi", "citing_doi"]).to_csv(
    "citations_doi.csv", index=False
)
