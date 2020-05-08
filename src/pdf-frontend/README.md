# PDF frontend for Record Sponge

This frontend is designed to batch process many names and output the analyses as one PDF per person.

## Usage

1. Run `pipenv install`
2. Install `wkhtmltopdf` (`apt-get install wkhtmltopdf` on Debian/Ubuntu)
3. Drop a csv file into source/ with the following headers: "First Name", "Last Name", "Middle", "First Short", "Last Short", "Birth Date", "Officer"
4. Launch the backend on http://localhost:5000 (`make up` does this by default)
5. Run `pipenv run python3 script.py`

## Notes

The "Officer" field is probably specific to the original work order this frontend was built for. The "First Name" and "Last Name" fields are used for display at the top of the PDF while the "First Short", "Middle", and "Last Short" fields are used for the query.