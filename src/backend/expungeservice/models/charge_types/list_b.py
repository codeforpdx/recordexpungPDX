from expungeservice.models.charge_types.base_charge import BaseCharge


class ListB(BaseCharge):

    def __init__(self, **kwargs):
        super(ListB, self).__init__(**kwargs)
