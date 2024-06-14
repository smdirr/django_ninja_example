from django.test import TestCase, Client
from django.urls import reverse


class TestPerson(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        my_pass = "devtestlocal"
        data = {
            "first_name": "Thomas",
            "last_name": "Anderson",
            "email": "tand@mail.me",
            "password": f"{my_pass}",
            "confirm_password": f"{my_pass}",
        }
        self.client.post(
            reverse("register"), data=data, content_type="application/json"
        )
        token = self.client.post(
            reverse("token_obtain_pair"),
            {"username": data.get("email"), "password": f"{my_pass}"},
            content_type="application/json",
        )
        self.access_token = token.json().get("access")

    def test_request_ok(self):

        response = self.client.get(
            reverse("api:person_list"),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)

    def test_request_invalid(self):

        response = self.client.get(
            reverse("api:person_list"),
            headers={"Authorization": "Bearer 1Nv4l1d70k3n"},
        )

        self.assertEqual(response.status_code, 401)
