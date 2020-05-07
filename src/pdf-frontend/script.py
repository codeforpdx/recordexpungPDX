import json
from functools import partial
import pandas as pd
from markdown_to_pdf import MarkdownToPDF
from auth import Auth
from serializer import Serializer


def dump_pdf(alias, record, filename):
    markdown = Serializer.serialize(alias, record)
    MarkdownToPDF.to_pdf(filename, "Expungement analysis", markdown)


def handle_person(client, row):
    alias = {
        "first_name": row["First Name"],
        "last_name": row["Last Name"],
        "birth_date": row["Birth Date"],
        "middle_name": "",
    }
    aliases = [alias]
    response = client.post("http://localhost:5000/api/search", json={"aliases": aliases})
    record = json.loads(response.text)["record"]
    dump_pdf(
        alias, record, filename=f"""output/{alias["first_name"]}_{alias["last_name"]}.pdf""",
    )


def search_and_dump_many_records(source_filename="source/cjpp.csv"):
    df = pd.read_csv(source_filename)
    cleaned_df = df[["First Name", "Last Name", "Birth Date", "Officer"]]  # TODO: Check unique of first/last name
    client = Auth.get_authenticated_client()
    cleaned_df.apply(partial(handle_person, client), axis="columns")


if __name__ == "__main__":
    search_and_dump_many_records()
