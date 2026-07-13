from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserCreate, UserLogin
from security import verify_password, create_access_token
import crud

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register_user(user: UserCreate):
    allowed_roles = [
    "Admin",
    "Employee",
    "Viewer"
]

    if user.role not in allowed_roles:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )
    
    user_id = crud.create_user(user)
    return {
        "message": "User registered successfully",
        "user_id": user_id
        }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = crud.get_user_by_username(
        form_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    if user["is_active"] == 0:

        raise HTTPException(
            status_code=403,
            detail="User account is disabled"
        )


    token = create_access_token(
        {
            "sub": user["username"]
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }