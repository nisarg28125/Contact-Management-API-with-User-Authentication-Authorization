from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from security import SECRET_KEY, ALGORITHM

import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_role(allowed_roles: list):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        print("Current User:", current_user)
        print("User Role:", current_user["role"])
        print("Allowed Roles:", allowed_roles)

        if current_user["role"] not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return role_checker