import json
from functools import partial
from expungeservice.serializer import ExpungeModelEncoder
import pandas as pd
from markdown_to_pdf import MarkdownToPDF
from auth import Auth


def generate_formatted_summary_text(record):
    # TODO:
    # open_cases_block = gen_open_cases_block(record)
    # ineligible_charges_block = gen_ineligible_charges_block(record)
    # future_eligible_block = gen_future_eligible_block(record)
    # needs_more_analysis_block = gen_needs_more_analysis_block(record)
    return json.dumps(record["summary"], indent=4, cls=ExpungeModelEncoder)


def dump_pdf(record, filename):
    markdown = generate_formatted_summary_text(record)
    MarkdownToPDF.to_pdf(filename, "Expungement analysis", markdown)


def handle_person(client, row):
    try:
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
            record, filename=f"""output/{alias["first_name"]}_{alias["last_name"]}.pdf""",
        )
    except Exception as ex:
        print("error:", ex)


def search_and_dump_many_records(source_filename="source/cjpp.csv"):
    df = pd.read_csv(source_filename)
    cleaned_df = df[["First Name", "Last Name", "Birth Date", "Officer"]]  # TODO: Check unique of first/last name
    client = Auth.get_authenticated_client()
    cleaned_df.apply(partial(handle_person, client), axis="columns")


if __name__ == "__main__":
    search_and_dump_many_records()
