"""
Import GEHA data and output to .csv
"""

import os, more_itertools, sys, csv


def process_file(path, file):
    os.chdir(path)

    with open(file, "r", encoding="latin-1") as data:
        for line, next_line in more_itertools.pairwise(data):

            if line.startswith("Member ID:"):       # When this text is seen,
                is_claim_header = True             # it marks the start of a claim summary
                claim_header = []                  # and a new claim_header is created

            if is_claim_header:
                if line.startswith("Member ID:") or \
                        line.startswith("Patient DOB:") or \
                        line.startswith("Patient Acct. No.:") or \
                        line.startswith("Claim Number:") or \
                        line.startswith("Status:") or \
                        line.startswith("Processed Date:") or \
                        line.startswith("EOB:"):
                    claim_header.append(line.split(" ")[-1].rstrip())
                elif line.startswith("Patient Name:"):
                    claim_header.append(line.split(" ")[-2].rstrip())
                if line.startswith("EOB: "):                               # When this text is seen,
                    is_claim_header = False                                # it marks the end of a claim header
                continue

            # if not is_claim_header:
            #     if not(line.startswith("Allowable") or
            #            line.startswith("Deductible") or
            #            line.startswith("Copay / Coinsurance") or
            #            line.startswith("Benefit") or
            #            line.startswith("Summary")):
            #         continue
            #     elif not(line.startswith("Date of Service") or
            #              line.startswith("Total Charges") or
            #              line.startswith("Max Allowed PPO Charges") or
            #              line.startswith("Not Covered") or
            #              line.startswith("Note")):
            #         claim_header.append(line.rstrip())


def main():
    """
    Test function for words library
    :return: nothing
    """
    process_file(r"C:\Users\JohnM\Desktop", "GEHA Data.txt")


if __name__ == "__main__":
    print(__name__)
    main()
    exit(0)