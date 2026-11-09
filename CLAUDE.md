# Working in this repo

## Data objects

Every dataclass in `src/backend/expungeservice/models/` is defined without field defaults, so
every field is required at instantiation. When a model gains a field, each place that builds the
object names the new value: the crawler, the editor, the demo records, and the test factories and
fixtures. A constructor that would otherwise fall back to a silent default is the point of the
rule.
