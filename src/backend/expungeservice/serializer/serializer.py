import flask
import expungeservice


class ExpungeModelEncoder(flask.json.JSONEncoder):


    def default(self, o):
        if isinstance(o, expungeservice.models.record.Record):
            return o.__dict__()

        else:
            return flask.json.JSONEncoder.default(self, o)
