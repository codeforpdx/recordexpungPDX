import json
from functools import partial
from pathlib import Path

import pandas as pd
from markdown_to_pdf import MarkdownToPDF
from auth import Auth
from serializer import Serializer


def dump_pdf(record, filename, name, birth_date, officer):
    markdown = Serializer.serialize(record, name, birth_date, officer)
    MarkdownToPDF.to_pdf(filename, "Expungement analysis", markdown)


def handle_person(client, row):
    alias = {
        "first_name": row.get("First Short", ""),
        "last_name": row.get("Last Short", ""),
        "birth_date": row.get("Birth Date", ""),
        "middle_name": row.get("Middle", ""),
    }
    aliases = [alias]
    response = client.post("http://localhost:5000/api/search", json={"aliases": aliases})
    record = json.loads(response.text)["record"]
    first_name = row.get("First Name", "").upper()
    last_name = row.get("Last Name", "").upper()
    name = f"{first_name} {last_name}"
    birth_date = row.get("Birth Date", "")
    officer = row.get("Officer", "").upper()
    dump_pdf(record, f"""output/{first_name}_{last_name}_{officer}.pdf""", name, birth_date, officer)


def search_and_dump_many_records(source_filename="source/cjpp.csv"):
    Path("output/").mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source_filename)
    cleaned_df = df[["First Name", "Last Name", "Middle", "First Short", "Last Short", "Birth Date", "Officer"]].fillna(
        ""
    )  # TODO: Check unique of first/last name
    client = Auth.get_authenticated_client()
    cleaned_df.apply(partial(handle_person, client), axis="columns")


if __name__ == "__main__":
    search_and_dump_many_records()
