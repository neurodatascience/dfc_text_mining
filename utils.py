from collections.abc import Sequence
import pathlib
import sqlite3
import sys
import zlib

import pandas as pd
import requests


def _get_pmcids_archive() -> pathlib.Path:
    archive_path = pathlib.Path("PMC-ids.csv.gz")
    if archive_path.is_file():
        return archive_path
    try:
        resp = requests.get(
            "https://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz"
        )
        resp.raise_for_status()
        archive_path.write_bytes(resp.content)
        return archive_path
    except Exception:
        if archive_path.is_file():
            archive_path.unlink()


def _get_pmcids_csv() -> pathlib.Path:
    pmcids_csv = pathlib.Path("PMC-ids.csv")
    if pmcids_csv.is_file():
        return pmcids_csv
    gzipped_csv = _get_pmcids_archive()
    gzipped_data = gzipped_csv.read_bytes()
    gunzipped_data = zlib.decompress(gzipped_data, wbits=31)
    pmcids_csv.write_bytes(gunzipped_data)
    return pmcids_csv


def _get_pmcids_db() -> pathlib.Path:
    database = pathlib.Path("pmcids.sqlite3")
    if database.is_file():
        return database
    pmcids_csv = _get_pmcids_csv()
    pmcids = pd.read_csv(pmcids_csv, dtype=str)
    connection = sqlite3.connect(database)
    pmcids.to_sql("pmcids", connection)
    return database


def doi_to_pmcid(doi: str) -> dict | None:
    db = _get_pmcids_db()
    with sqlite3.connect(db) as connection:
        connection.row_factory = sqlite3.Row
        res = connection.execute(
            "SELECT * from pmcids WHERE DOI = ?", (doi,)
        ).fetchone()
    if res is None:
        return None
    return dict(res)


def multi_doi_to_pmcid(all_dois: Sequence[str]) -> pd.DataFrame:
    db = _get_pmcids_db()
    with sqlite3.connect(db) as connection:
        df = pd.read_sql("select * from pmcids", connection)
    df.dropna(subset=("DOI", "PMCID"), inplace=True)
    df.set_index("DOI", inplace=True)
    intersection = df.index.intersection(all_dois)
    return df.loc[intersection].reset_index()
