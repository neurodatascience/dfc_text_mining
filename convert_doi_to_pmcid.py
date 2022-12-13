import sys

import utils

dois = [doi.strip() for doi in sys.stdin]
pmcids = utils.doi_to_pmcid(dois)
sys.stdout.write("\n".join(map(str, pmcids["PMCID"])))
sys.stdout.write("\n")
