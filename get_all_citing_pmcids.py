import json
import pathlib

import utils

citation_data = json.loads(pathlib.Path("opencitations_data.json").read_text())
all_dois = []
for paper_info in citation_data:
    for citation_info in paper_info:
        all_dois.append(citation_info["citing"])

print(len(all_dois))
df = utils.multi_doi_to_pmcid(all_dois)
df["PMCID"].str.lstrip("PMC").astype(int).to_csv(
    "dfc_citing_pmcids.txt", header=None, index=False
)
