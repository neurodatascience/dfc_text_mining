.import --csv PMC-ids.csv pmcids
CREATE INDEX doi_idx ON pmcids (DOI);
CREATE INDEX pmcid_idx ON pmcids (PMCID);
