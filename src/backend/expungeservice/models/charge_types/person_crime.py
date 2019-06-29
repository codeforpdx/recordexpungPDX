from expungeservice.models.charge_types.base_charge import BaseCharge


class PersonCrime(BaseCharge):

    def __init__(self, **kwargs):
        super(PersonCrime, self).__init__(**kwargs)
