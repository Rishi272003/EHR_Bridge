from abc import ABC
class SuperClient(ABC):
    def __init__(self):
        self.connection_obj = None
        self.base_url = None
        self.auth_url = None
        self.auth_token = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.payload = {}

    def build_url(self):
        """
        Build URL for request.
        """
        raise NotImplementedError

    def build_headers(self):
        """
        Build headers for request.
        """
        raise NotImplementedError

    def build_payload(self):
        """
        Build payload for request.
        """
        raise NotImplementedError

    def authenticate(self):
        """
        Authenticate user with given username and password.
        """
        raise NotImplementedError

    def refresh_token(self):
        """
        Refresh token.
        """
        raise NotImplementedError

    def persist_token(self):
        """
        Persist token to file.
        """
        raise NotImplementedError

    def read_token(self):
        """
        Read stored token from file.
        """
        raise NotImplementedError

    def get(self):
        """
        GET method to get data from given URL.
        """
        raise NotImplementedError

    def post(self):
        """
        POST method to post data to given URL.
        """
        raise NotImplementedError

    def put(self):
        """
        PUT method to put data to given URL.
        """
        raise NotImplementedError

    def patch(self):
        """
        PATCH method to patch data to given URL.
        """
        raise NotImplementedError

    def delete(self):
        """
        DELETE method to delete data to given URL.
        """
        raise NotImplementedError
