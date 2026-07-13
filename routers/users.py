from fastapi import APIRouter, Depends, HTTPException
from dependencies import require_role, get_current_user
import crud
import schemas
from security import hash_password, verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def get_my_profile(
    current_user = Depends(
        require_role(
            ["Admin","Employee","Viewer"]
        )
    )
):

    return {
        "message": "All contacts",
        "user": current_user["username"]
    }

@router.get("/")
def get_all_users(

    current_user=Depends(
        require_role(
            ["Admin"]
        )
    )

):

    return crud.get_all_users()


@router.put("/change-password")
def change_password(

    passwords: schemas.ChangePassword,

    current_user=Depends(get_current_user)

):

    if not verify_password(

        passwords.current_password,

        current_user["password_hash"]

    ):

        raise HTTPException(

            status_code=401,

            detail="Current password is incorrect"

        )


    new_hash = hash_password(

        passwords.new_password

    )


    crud.change_password(

        current_user["user_id"],

        new_hash

    )


    return {

        "message": "Password changed successfully"

    }

@router.put("/{user_id}/disable")
def disable_user(

    user_id: str,

    current_user=Depends(
        require_role(["Admin"])
    )

):

    success = crud.disable_user(user_id)

    if not success:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User disabled successfully"
    }

@router.put("/{user_id}/enable")
def enable_user(

    user_id: str,

    current_user=Depends(
        require_role(["Admin"])
    )

):

    success = crud.enable_user(user_id)

    if not success:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User enabled successfully"
    }

@router.delete("/{user_id}")
def delete_user(

    user_id: str,

    current_user=Depends(
        require_role(["Admin"])
    )

):

    success = crud.delete_user(user_id)

    if not success:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }