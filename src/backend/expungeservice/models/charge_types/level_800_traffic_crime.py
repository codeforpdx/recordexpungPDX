from expungeservice.models.charge_types.base_charge import BaseCharge


class Level800TrafficCrime(BaseCharge):

    def __init__(self, **kwargs):
        super(Level800TrafficCrime, self).__init__(**kwargs)
