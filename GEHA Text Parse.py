"""
Import GEHA data and output to .csv
"""

import os, more_itertools, sys, csv


def process_file(path, file):

    os.chdir(path)
    section = ''
    claim_detail = []
    claim_detail_output = []
    claim_header = []
    claim_header_output = []

    with open(file, "r", encoding="latin-1") as data:
        for line, next_line in more_itertools.pairwise(data):

            section = determine_section(line, section)

            if section == "header":
                if line.startswith("Claim Number:"):
                    claim_number = line.split(" ")[-1].rstrip()
                if line.startswith("Patient DOB:") or \
                        line.startswith("Patient Acct. No.:") or \
                        line.startswith("Status:") or \
                        line.startswith("Processed Date:"):
                    claim_header.append(line.split(" ")[-1].rstrip())
                if line.startswith("Processed Date:"):              # When this text is seen,
                    claim_header_output.append(claim_header)        # it marks the end
                    claim_header.clear()                            # of the header section
                    section = "claim_detail"                        # and the start of the claim detail
                    #print(claim_header_output)
            elif section == "claim_detail":
                if not claim_detail:
                    claim_detail.append(next_line.rstrip())
                if line.startswith("Date of Service") or \
                        line.startswith("Total Charges") or \
                        line.startswith("Max Allowed PPO Charges") or \
                        line.startswith("Not Covered") or \
                        line.startswith("Note") or \
                        line.startswith("Allowable") or \
                        line.startswith("Deductible") or \
                        line.startswith("Copay / Coinsurance") or \
                        line.startswith("Benefit"):
                    claim_detail.append(next_line.rstrip())
                if line.startswith("Benefit"):
                    print([len(claim_detail)] + [claim_number] + claim_detail)
                    claim_detail_output.append(claim_detail)
                    claim_detail.clear()
            elif section == "summary":
                pass


def determine_section(line, section):
    if ":" in line and "EOB: View" not in line:   # When this text is seen,
        return "header"                 # it marks the start of a claim summary
    elif line == "Summary\n":
        return "summary"
    else:
        return section


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