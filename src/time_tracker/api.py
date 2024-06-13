from ninja import NinjaAPI
from person.api import router as person_router
from time_tracker.security import JWTAuth

api = NinjaAPI(auth=JWTAuth(), urls_namespace="api")

api.add_router("/person/", person_router)
