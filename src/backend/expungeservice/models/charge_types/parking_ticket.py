from expungeservice.models.charge_types.base_charge import BaseCharge


class ParkingTicket(BaseCharge):

    def __init__(self, **kwargs):
        super(ParkingTicket, self).__init__(**kwargs)
