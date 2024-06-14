from django.test import TestCase, Client
from django.urls import reverse
from person.models import Person


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

    def test_get_person(self):

        Person.objects.create(first_name="John", last_name="Doe", email="john@test.com")
        Person.objects.create(
            first_name="Alice", last_name="Silver", email="asilver@test.com"
        )

        response = self.client.get(
            reverse("api:person_list"),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["first_name"], "John")
        self.assertEqual(response.json()[0]["email"], "john@test.com")

    def test_create_person(self):

        data = {
            "first_name": "Jenifer",
            "last_name": "Lopez",
            "email": "jlo@mail.com",
            "birth_date": "1970-03-21",
        }
        response = self.client.post(
            reverse("api:person_create"),
            data=data,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json().get("id"), 0)

    def test_update_person(self):
        data = {
            "first_name": "Jenifer",
            "last_name": "Lopez",
            "email": "jlo@mail.com",
            "birth_date": "1970-03-21",
        }
        response = self.client.post(
            reverse("api:person_create"),
            data=data,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        id = response.json().get("id")
        url = reverse("api:person_edit", kwargs={"person_id": id})
        data["last_name"] = "López"
        response = self.client.put(
            url,
            data=data,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("success"), True)
        person = self.client.get(
            reverse("api:person_get", args=[id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(person.status_code, 200)
        self.assertEqual(person.json()["last_name"], "López")

    def test_person_delete(self):
        data = {
            "first_name": "Jenifer",
            "last_name": "Lopez",
            "email": "jlo@mail.com",
            "birth_date": "1970-03-21",
        }
        response = self.client.post(
            reverse("api:person_create"),
            data=data,
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        id = response.json().get("id")
        url = reverse("api:person_delete", kwargs={"person_id": id})
        response = self.client.delete(
            url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("success"), True)

    def test_get_person_401(self):
        response = self.client.get(reverse("api:person_list"))
        self.assertEqual(response.status_code, 401)

    def test_get_persons(self):

        Person.objects.create(first_name="John", last_name="Doe", email="john@test.com")

        response = self.client.get(
            reverse("api:person_list"),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["email"], "john@test.com")

    def test_retrieve_person(self):

        my_person = Person.objects.create(
            first_name="Juan", last_name="Fangio", email="jf@test.com"
        )
        response = self.client.get(
            reverse("api:person_get", args=[my_person.id]),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "jf@test.com")

    def test_str_person(self):

        person = Person.objects.create(
            first_name="John", last_name="Doe", email="john@test.com"
        )
        self.assertEqual(str(person), "Doe, John")

    def test_register_pass_no_match(self):
        data = {
            "first_name": "Mick",
            "last_name": "Jaegger",
            "email": "mj@mail.me",
            "password": "match",
            "confirm_password": "no match",
        }
        response = self.client.post(
            reverse("register"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "Passwords do not match")

    def test_register_username_already_exist(self):
        data = {
            "first_name": "Mick",
            "last_name": "Jaegger",
            "email": "tand@mail.me",
            "password": "test@1234",
            "confirm_password": "test@1234",
        }
        response = self.client.post(
            reverse("register"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "Username already taken")

    def test_register_invalid_body(self):
        invalid_json = "{email: 'test@example.com', password: 'pass123', confirm_password: 'pass123'"
        response = self.client.post(
            reverse("register"), data=invalid_json, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("error"), "Invalid JSON")

    def test_register_invalid_request_method(self):

        response = self.client.get(reverse("register"), content_type="application/json")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json().get("error"), "Invalid request method")
