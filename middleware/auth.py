from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import jwt
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/account/login")

def get_current_user(token: str = Security(oauth2_scheme)):
    print(f"Token received: {token}")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")