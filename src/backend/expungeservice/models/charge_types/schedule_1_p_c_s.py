from expungeservice.models.charge_types.base_charge import BaseCharge


class Schedule1PCS(BaseCharge):

    def __init__(self, **kwargs):
        super(Schedule1PCS, self).__init__(**kwargs)
