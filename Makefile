.PHONY: all download clean

all: dfc_citing_pmcids.txt

PMC-ids.csv:
	wget "https://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz"
	gunzip PMC-ids.csv.gz

pmcids.sqlite3: PMC-ids.csv
	sqlite3 $@ '.read create_db.sql'

opencitations_sparql_data.json: dfc_dois.txt
	python3 collect_citations_via_sparql.py

opencitations_rest_data.json: dfc_dois.txt
	python3 collect_citations_via_rest.py

citations_doi.csv: dfc_dois.txt
	python3 collect_citations_via_sparql.py

dfc_citing_pmcids.txt: citations_doi.csv pmcids.sqlite3
	python3 get_all_citing_pmcids.py

download: dfc_citing_pmcids.txt
	export PUBGET_DATA_DIR="$${PUBGET_DATA_DIR:-$$(pwd)}"
	pubget run --pmcids_file $< --labelbuddy

clean:
	rm -f opencitations_rest_data.json opencitations_sparql_data.json opencitations_data.json citations_doi.csv dfc_citing_pmcids.txt

clean_all: clean
	rm -f PMC-ids.csv.gz PMC-ids.csv pmcids.sqlite3
