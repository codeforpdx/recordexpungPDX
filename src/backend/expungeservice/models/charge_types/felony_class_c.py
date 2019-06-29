from expungeservice.models.charge_types.base_charge import BaseCharge


class FelonyClassC(BaseCharge):

    def __init__(self, **kwargs):
        super(FelonyClassC, self).__init__(**kwargs)
