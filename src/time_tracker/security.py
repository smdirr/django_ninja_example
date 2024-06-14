from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError):
            return None
        return token
