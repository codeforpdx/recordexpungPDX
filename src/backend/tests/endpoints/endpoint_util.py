import expungeservice


class EndpointShared:
    def __init__(self):
        self.app = expungeservice.create_app("development")
        self.client = self.app.test_client()
