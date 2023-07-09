import os
import uuid
import jwt
from datetime import (
    datetime,
    timedelta
)
from django.shortcuts import get_object_or_404

from common.config.consts import ACCESS_JWT_ALGORITHM, ACCESS_EXP
from user.models import DanbiUser


def create_user_key() -> str:
    user_key = None
    while not user_key:
        try:
            candidate = str(uuid.uuid4())
            user = DanbiUser.objects.get(user_key = candidate)

        except DanbiUser.DoesNotExist:
            user_key = candidate

    return user_key

def create_access_token(user):
    data = dict(
        user_key = user.user_key,
        name = user.username,
        team = user.team,
        exp = datetime.utcnow() + timedelta(seconds=ACCESS_EXP)
    )

    token = jwt.encode(data, key=os.environ.get('JWT_SECRET'), algorithm=ACCESS_JWT_ALGORITHM)
    expired_date = data['exp']

    return token, expired_date

def token_decode(access_token):
    try:
        access_token = access_token.replace('Bearer ', '')
        payload = jwt.decode(access_token, key=os.environ.get('JWT_SECRET'), algorithms=ACCESS_JWT_ALGORITHM)

    except jwt.ExpiredSignatureError:
        raise ValueError()

    except jwt.DecodeError:
        raise ValueError()

    return payload


def user_check(token):
    token_info = token_decode(access_token = token)
    user_info = token_info['user_key']
    user = get_object_or_404(DanbiUser, user_key=user_info)
    
    return user
