from expungeservice.models.charge_types.base_charge import BaseCharge


class FelonyClassA(BaseCharge):

    def __init__(self, **kwargs):
        super(FelonyClassA, self).__init__(**kwargs)
