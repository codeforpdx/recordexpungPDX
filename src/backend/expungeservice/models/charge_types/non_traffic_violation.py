from expungeservice.models.charge_types.base_charge import BaseCharge


class NonTrafficViolation(BaseCharge):

    def __init__(self, **kwargs):
        super(NonTrafficViolation, self).__init__(**kwargs)
