from ninja import NinjaAPI
from person.api import router as person_router


api = NinjaAPI()

api.add_router("/person/", person_router)
