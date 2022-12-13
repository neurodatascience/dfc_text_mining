extract functional connectivity methods from papers

installation:

```
pip install -r requirements.txt
```

to fetch the PMCIDs of papers that cite those listed in `dfc_dois.txt`:

```
make
```

to also download those papers, 
```
export PUBGET_DATA_DIR="/where/you/want/to/store/pubget/data/"
```
(optional, pwd will be used otherwise, see [pubget documentation](https://neuroquery.github.io/pubget/) for other configuration options)
```
make download
```

to start annotating papers:

[install labelbuddy](https://jeromedockes.github.io/labelbuddy/labelbuddy/current/installation/)
go to the **pubget** data dir created by the previous command, navigate to `pmcidList_<SOME HASH>/subset_allArticles_labelbuddyData`

```
labelbuddy dfc_papers.labelbuddy --import-docs documents_00001.jsonl
labelbuddy dfc_papers.labelbuddy &
```

create labels and start annotating
