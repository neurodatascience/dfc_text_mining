import json
import pathlib

import pandas as pd

import utils

all_dois = pd.read_csv("citations_doi.csv")["citing_doi"].values
print(f"Found DOIs for {len(all_dois)} papers.")
df = utils.doi_to_pmcid(all_dois)
print(f"{len(df)} papers have a PMC ID.")
df["PMCID"].str.lstrip("PMC").astype(int).to_csv(
    "dfc_citing_pmcids.txt", header=None, index=False
)
