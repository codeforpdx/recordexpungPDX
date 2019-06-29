from expungeservice.models.charge_types.base_charge import BaseCharge


class FelonyClassB(BaseCharge):

    def __init__(self, **kwargs):
        super(FelonyClassB, self).__init__(**kwargs)
