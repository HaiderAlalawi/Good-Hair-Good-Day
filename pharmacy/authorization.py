from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from jose import jwt, JWTError

from config import settings

User = get_user_model()



class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_username = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms='HS256')
        except JWTError:
            return 401,{'token': 'unauthorized'}
        if user_username:
            return 200, user_username

def create_token_for_user(user):
    token = jwt.encode({'username': str(user.username)},
                    key=settings.SECRET_KEY, algorithm='HS256')
    return str(token)