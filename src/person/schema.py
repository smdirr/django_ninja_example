from datetime import date
from ninja import Schema


class PersonIn(Schema):
    first_name: str
    last_name: str
    email: str
    birth_date: date = None


class PersonOut(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    birth_date: date = None
