.PHONY: all download

all: dfc_citing_pmcids.txt

PMC-ids.csv:
	wget "https://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz"
	gunzip PMC-ids.csv.gz

pmcids.sqlite3: PMC-ids.csv
	sqlite3 $@ '.read create_db.sql'

opencitations_data.json: dfc_dois.txt
	python3 collect_citations.py

dfc_citing_pmcids.txt: opencitations_data.json pmcids.sqlite3
	python3 get_all_citing_pmcids.py

download: dfc_citing_pmcids.txt
	export PUBGET_DATA_DIR="$${PUBGET_DATA_DIR:-$$(pwd)}"
	pubget run --pmcids_file $< --labelbuddy
