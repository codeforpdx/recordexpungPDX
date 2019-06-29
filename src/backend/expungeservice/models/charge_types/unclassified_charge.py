from expungeservice.models.charge_types.base_charge import BaseCharge


class UnclassifiedCharge(BaseCharge):

    def __init__(self, **kwargs):
        super(UnclassifiedCharge, self).__init__(**kwargs)
        if self.acquitted():
            self.expungement_result.set_type_eligibility(True)
            self.expungement_result.set_reason('Eligible under 137.225(1)(b)')
        else:
            self.expungement_result.set_reason('Examine')
