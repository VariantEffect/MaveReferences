"""

"""
import csv
import idutils


def format_md_link(val, scheme, url_scheme="https"):
    """Returns a properly-formatted markdown link for the identifier and scheme.
    """
    return f"[{val}]({idutils.to_url(val, scheme, url_scheme=url_scheme)})"


if __name__ == "__main__":
    # keep the README text before the table
    intro = list()
    with open("README.md", "r") as infile:
        for line in infile:
            if line.startswith("|"):  # start of table
                break
            else:
                intro.append(line)

    # generate the new README
    records = list()
    with open("maverefs.tsv", mode="r", newline="") as infile, open("README.md", mode="w", newline="") as outfile:
        # rewrite the introductory text
        for line in intro:
            print(line, end="", file=outfile)

        # regenerate the table line-by-line
        reader = csv.DictReader(infile, delimiter="\t")
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter="|", lineterminator="|\n")
        print("|", end="", file=outfile)
        writer.writeheader()
        print("|---" * len(reader.fieldnames) + "|\n", end="", file=outfile)
        for row in reader:
            if idutils.is_pmid(row["PMID"]):
                row["PMID"] = format_md_link(row["PMID"], "pmid")
            if idutils.is_doi(row["DOI"]):
                row["DOI"] = format_md_link(row["DOI"], "doi")
            raw_data_schemes = idutils.detect_identifier_schemes(row["Raw Data"])
            if len(raw_data_schemes) == 1:  # uniquely identified the raw data
                row["Raw Data"] = format_md_link(row["Raw Data"], raw_data_schemes[0])
            print("|", end="", file=outfile)
            writer.writerow(row)
