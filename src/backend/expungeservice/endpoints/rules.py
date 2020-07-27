from flask.views import MethodView
from flask import make_response

from expungeservice.generator import get_charge_classes


class Rules(MethodView):
    def get(self):
        return make_response(
            {
                "charge_types": [
                    {
                        "charge_type_class_name": charge_class.__name__,
                        "charge_type_name": charge_class.type_name,
                        "expungement_rules": charge_class.expungement_rules,
                    }
                    for charge_class in get_charge_classes()
                ]
            }
            # TODO: add "time_rules"
        )


def register(app):
    app.add_url_rule("/api/rules", view_func=Rules.as_view("rules"))
