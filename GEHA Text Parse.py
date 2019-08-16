"""
Import GEHA data and output to .csv
"""

import os, sys, csv

def process_file(path, file):
    os.chdir(path)

    with open(file, "r", encoding="latin-1") as data:
        for line in data:

            if line.startswith("Member ID:"):       # When this text is seen,
                is_claim_summary = True             # it marks the start of a claim summary
                claim_summary = []                  # and a new claim_summary is created

            if is_claim_summary:
                if line.startswith("Member ID:") or \
                    line.startswith("Patient DOB:") or \
                    line.startswith("Patient Acct. No.:") or \
                    line.startswith("Claim Number:") or \
                    line.startswith("Status:") or \
                    line.startswith("Processed Date:") or \
                    line.startswith("EOB:"):
                        claim_summary.append(line.split(" ")[-1])
                elif line.startswith("Patient Name:"):
                        claim_summary.append(line.split(" ")[-2])
                elif line.startswith("BALANCE OF COVERED CHARGES APPLIED"):     # When this text is seen,
                    is_claim_summary = False                                    # it marks the end of a claim summary
                    continue
                elif line == "Date of Service" or \
                    line == "Total Charges" or \
                    line == "Max Allowed PPO Charges" or \
                    line == "Not Covered" or \
                    line == "Note":
                        continue
                else:
                    claim_summary.append(line)

            if line.contains(":"):
                continue
            if line.startswith("Date of Service") or \
                line.startswith("Total Charges") or \
                line.startswith("Date of Service") or \:
                continue



    #with open(file.split(".")[0] + "Clean.csv", "w", encoding='ascii') as newData:
        # write

def main():
    """
    Test function for words library
    :return: nothing
    """
    process_file(r"C:\Users\JohnM\Desktop", "GEHA Data")

if __name__ == "__main__":
    print(__name__)
    main()
    exit(0)