import json
import pathlib

import utils

citation_data = json.loads(pathlib.Path("opencitations_data.json").read_text())
all_dois = []
for paper_info in citation_data:
    for citation_info in paper_info:
        all_dois.append(citation_info["citing"])

print(f"Found DOIs for {len(all_dois)} papers.")
df = utils.doi_to_pmcid(all_dois)
print(f"{len(df)} papers have a PMC ID.")
df["PMCID"].str.lstrip("PMC").astype(int).to_csv(
    "dfc_citing_pmcids.txt", header=None, index=False
)
