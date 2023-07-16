from ninja import Router
from pharmacy.authorization import *
from pharmacy.schema import *

sign_in_router = Router(tags=['SignIn'])

@sign_in_router.post("/signin",response={
    200: AuthOut,
    404: ErrorCode,
    401: ErrorCode,
    403: ErrorCode,
})
def signin(request, username:str, password:str):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    else:
        if user.is_active:
            if user.check_password(password):
                token = create_token_for_user(user)
                return {
                    'token': token,
                }
            else:
                return 401,{'detail': 'password incorrect'}
        return 403,{'detail': 'User is not active'}    
    if not user:
        return 404, {'detail': 'User is not registered'}