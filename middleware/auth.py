from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from config.config import settings
from schemas.user import UserData
from db.database import collection_user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserData:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])

        user = await collection_user.find_one({'email': payload['sub']})
        if (user):
            return user
        raise HTTPException(404, f"User not found")
    except (jwt.JWTError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
