# Simple script to calculate the number of variants per year

import sys
import pandas as pd


def get_total(s):
    """Convert a semicolon-separated list of integers into the sum of that list.

    Helper function for multi-target papers.

    Returns the integer if only one value is present.

    Returns 0 if the value of s is None or NA.
    """
    if s is None or pd.isna(s):
        return 0
    elif ";" in s:
        return sum(int(x) for x in s.split(";"))
    else:
        return int(s)


if __name__ == "__main__":
    # read the table
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    else:
        infile = "maverefs.tsv"
    df = pd.read_csv(infile, sep="\t")

    # calculate and store the number of variants per paper
    # keep the maximum of nt and aa variant counts if both are specified
    df["Variants (max)"] = 0
    for i, r in df.iterrows():
        df.loc[i, "Variants (max)"] = max(
            get_total(r["Variants (nt)"]), get_total(r["Variants (aa)"])
        )

    # calculate the sum of variants for each year
    result = df.groupby("Year")["Variants (max)"].sum()
    result.index = [
        int(x) for x in result.index
    ]  # convert years to ints instead of float
    result.index.name = "year"
    result.name = "variants"
    result = pd.DataFrame(result)
    result["cumulative_variants"] = result["variants"].cumsum()

    # write the result to stdout
    result.to_csv(sys.stdout)
