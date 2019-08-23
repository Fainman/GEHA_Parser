"""
Import GEHA data and output to .csv
"""

import os, more_itertools, sys, csv, pprint


def process_file(path, file):

    os.chdir(path)
    section = ''
    claim_detail = []
    claim_detail_output = []
    claim_header = []
    claim_header_output = []
    claim_summary = []
    claim_summary_output = []

    with open(file, "r", encoding="latin-1") as data:
        for line, next_line in more_itertools.pairwise(data):

            if determine_section(line) is not None:
                section = determine_section(line)

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
                    claim_header = []                               # of the header section
                    section = "claim_detail"                        # and the start of the claim detail
            elif section == "claim_detail":
                if not claim_detail and next_line != "Summary\n":
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
                    #print([len(claim_detail)] + [claim_number] + claim_detail)
                    claim_detail_output.append([claim_number] + claim_detail)
                    claim_detail = []
            elif section == "summary":
                if line.startswith("PAYEE	CHECK #	AMOUNT"):                   # If end of summary, do clean up
                    if next_line.startswith("Member ID: "):                     # If next line is member id,
                        claim_summary += ["", "", ""]                           # there's no info to obtain.
                    else:                                                       # Otherwise,
                        next_line = next_line.rstrip()                          # remove the \n
                        claim_summary += next_line.split("\t")                  # and obtain the data
                    claim_summary_output.append([claim_number] + claim_summary)     # Create output
                    claim_summary = []                                              # Reset it to [] for next time
                elif line.startswith("Benefits Payable") or \
                        line.startswith("Paid by Other Plan") or \
                        line.startswith("Other Plan Paid Adjustment") or \
                        line.startswith("Other Adjustment") or \
                        line.startswith("Other Adjustment Reason") or \
                        line.startswith("Total Paid by GEHA") or \
                        line.startswith("Patient Owes Provider"):
                    claim_summary.append(line.split("\t")[-1].rstrip())

    # Output to CSV
    with open('headers.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Patient DOB', 'Patient Acct. No.', 'Claim Number', 'Status', 'Processed Date'])
        for row in claim_header_output:
            csv_writer.writerow(row)
    with open('detail.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Provider Name', 'Date of Service', 'Total Charges', 'Max Allowed PPO Charges', 'Not Covered',
                            'Note', 'Allowable', 'Deductible', 'Copay / Coinsurance', 'Benefit'])
        for row in claim_detail_output:
            csv_writer.writerow(row)
    with open('summary.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Patient DOB', 'Patient Acct. No.', 'Claim Number', 'Status', 'Processed Date'])
        for row in claim_summary_output:
            csv_writer.writerow(row)


def determine_section(line):
    if ":" in line and "EOB: View" not in line:     # When this text is seen,
        return "header"                             # it marks the start of a claim summary
    elif line == "Summary\n":
        return "summary"
    else:
        return None                                 # No change


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