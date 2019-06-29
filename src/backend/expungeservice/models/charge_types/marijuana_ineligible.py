from expungeservice.models.charge_types.base_charge import BaseCharge


class MarijuanaIneligible(BaseCharge):

    def __init__(self, **kwargs):
        super(MarijuanaIneligible, self).__init__(**kwargs)
