from apis.api_client import ApiClient

class AuthAPI:
    def __init__(self):
        self.client = ApiClient()

    def login(self, email, password):
        return self.client.post("/auth/api/login", json={
            "email": email,
            "password": password
        })