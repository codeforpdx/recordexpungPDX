import json
from functools import partial
from pathlib import Path

import pandas as pd
from auth import Auth

from expungeservice.pdf.markdown_serializer import MarkdownSerializer
from expungeservice.pdf.markdown_to_pdf import MarkdownToPDF


def build_header(aliases, name, birth_date, officer):
    title = f"# EXPUNGEMENT ANALYSIS REPORT  \n"
    name = f"Name: {name}  \n" if name else ""
    dob = f"DOB: {birth_date}  \n" if birth_date else ""
    officer = f"Officer: {officer}  \n" if officer else ""
    header1 = title + name + dob + officer
    header2 = "## Search Terms  \n"
    for alias in aliases:
        name = f"{alias.get('first_name', '')} {alias.get('middle_name', '')} {alias.get('last_name', '')}".upper()
        name_line = f"Name: {name} " if name else ""
        dob = f"DOB: {alias.get('birth_date')}  \n" if alias.get("birth_date") else " \n"
        alias_line = name_line + dob
        header2 += alias_line
    return header1 + header2


def handle_person(output, client, row):
    alias = {
        "first_name": row.get("First Short", ""),
        "last_name": row.get("Last Short", ""),
        "birth_date": row.get("Birth Date", ""),
        "middle_name": "",
    }
    aliases = [alias]
    response = client.post("http://localhost:5000/api/search", json={"aliases": aliases})
    record = json.loads(response.text)["record"]
    first_name = row.get("First Name", "").upper()
    middle = row.get("Middle", "").upper()
    last_name = row.get("Last Name", "").upper()
    name = f"{first_name} {middle} {last_name}"
    birth_date = row.get("Birth Date", "")
    officer = row.get("Officer", "").upper()
    header = build_header(aliases, name, birth_date, officer)
    if record.get("cases"):
        print(f"PROCESSING ANALYSIS FOR {name}")
        source = MarkdownSerializer.to_markdown(record, header)
        pdf = MarkdownToPDF.to_pdf("Expungement analysis", source)
        Path(f"{output}/{officer}/").mkdir(parents=True, exist_ok=True)
        filename = f"{output}/{officer}/{first_name}_{last_name}_{officer}.pdf"
        with open(filename, "wb") as f:
            f.write(pdf)
    else:
        print(f"BLANK RECORD: {name} {aliases}")


def search_and_dump_many_records(source_filename="source/cjpp.csv", output="output/"):
    Path(output).mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source_filename)
    cleaned_df = df[["First Name", "Last Name", "Middle", "First Short", "Last Short", "Birth Date", "Officer"]].fillna(
        ""
    )  # TODO: Check unique of first/last name
    client = Auth.get_authenticated_client()
    cleaned_df.apply(partial(handle_person, output, client), axis="columns")


if __name__ == "__main__":
    search_and_dump_many_records("source/cjpp2.csv", "output2/")
