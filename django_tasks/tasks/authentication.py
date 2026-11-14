from typing import override
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken

from tasks.models import User

class JWTAuthentication(BaseAuthentication):

    @override
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if not header:
            return None
        if not header.startswith("Bearer "):
            return None
        token = header.split(" ")[1]
        try:
            validated_token = AccessToken(token)
            user = User.objects.get(id=validated_token["user_id"])
            user.is_authenticated = True
            return (user, validated_token)
        except InvalidToken:
            return None