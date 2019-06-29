from expungeservice.models.charge_types.base_charge import BaseCharge


class UnclassifiedCharge(BaseCharge):

    def __init__(self, **kwargs):
        super(UnclassifiedCharge, self).__init__(**kwargs)
