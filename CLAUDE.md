# Working in this repo

## Data objects

The data objects in `src/backend/expungeservice/models/` take every field at instantiation: no
field defaults. A new field is then named at every construction site, which for a case means the
crawler, the record parser, the editor's empty case, the demo records, the hypothesis generator,
and the test factories and fixtures. Charge types are the exception; their class attributes are
constants, not per-instance data.
