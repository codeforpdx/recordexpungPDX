from expungeservice.models.charge_types.base_charge import BaseCharge


class Misdemeanor(BaseCharge):

    def __init__(self, **kwargs):
        super(Misdemeanor, self).__init__(**kwargs)
