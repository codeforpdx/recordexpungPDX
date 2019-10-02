from expungeservice.models.charge_types.base_charge import BaseCharge


class ParkingTicket(BaseCharge):

    def __init__(self, **kwargs):
        super(ParkingTicket, self).__init__(**kwargs)
        self.expungement_result.set_type_eligibility(False)
        self.expungement_result.set_reason('Ineligible under 137.225(5)')

    def skip_analysis(self):
        return True
