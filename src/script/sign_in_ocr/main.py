import csv
import getopt
import os
import re
import shutil
import sys
from itertools import takewhile

from sign_in_ocr.ocr import CharacterReader
from sign_in_ocr.pdf_to_images import ImageConverter

from dotenv import load_dotenv


def run(pdf_file: str, output_folder: str):
    ImageConverter.pdftopil(pdf_file)
    rows = []
    for subdir, dirs, files in os.walk("tmp"):
        files.sort()
        files = [f for f in files if not f[0] == "."]
        for i, file in enumerate(files):
            file_path = os.path.join(subdir, file)
            text = CharacterReader.detect_document(file_path)
            elements = text.split(",")
            officer_name_possible = elements[9:15]
            officer_name = " ".join(reversed([e for e in officer_name_possible if e.isupper()])).strip()
            names_possible = elements[20:]
            cleaned_names_possible = [re.sub("(\d{7}|\d{8})\s\w{2}\s\d{4}", "", e) for e in names_possible]
            names = [e for e in cleaned_names_possible if e and (e.isupper() and not any(c.isdigit() for c in e))]
            name_pairs = list(zip(names[::2], names[1::2]))
            for last, first_middle in name_pairs:
                first, *middle = first_middle.strip().split(" ")
                middle_joined = " ".join(middle)
                middle_stripped = "".join(takewhile(lambda c: not c.isdigit(), list(middle_joined)))
                row = [first, middle_stripped, last, "", officer_name]
                rows.append(row)
                print(row)
    shutil.rmtree("tmp")
    with open(os.path.join(output_folder, "names.csv"), "wt") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["First Name", "Middle Name", "Last Name", "Birth Date", "Officer"])
        writer.writerows(rows)


def main(argv):
    inputfile = "data/sample.pdf"
    outputfile = "output2"
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("main.py -i <input_dir> -o <output_dir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("main.py -i <input_dir> -o <output_dir>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    run(inputfile, outputfile)


if __name__ == "__main__":
    load_dotenv()
    main(sys.argv[1:])
