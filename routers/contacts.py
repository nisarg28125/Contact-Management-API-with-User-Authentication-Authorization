from fastapi import APIRouter, Depends, HTTPException

import crud
import schemas

from dependencies import get_current_user, require_role


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)

@router.get("/")
def get_contacts(

    current_user=Depends(
        require_role(
            ["Admin", "Employee", "Viewer"]
        )
    )

):

    return crud.get_all_contacts()

@router.post("/")
def create_contact(

    contact: schemas.ContactCreate,

    current_user=Depends(
        require_role(
            ["Admin", "Employee"]
        )
    )

):

    contact_id = crud.create_contact(contact)

    return {
        "message": "Contact created successfully",
        "contact_id": contact_id
    }


@router.get("/{contact_id}")
def get_contact(

    contact_id: str,

    current_user=Depends(
        require_role(
            ["Admin", "Employee", "Viewer"]
        )
    )

):

    contact = crud.get_contact_by_id(contact_id)

    if contact is None:

        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return contact


@router.put("/{contact_id}")
def update_contact(

    contact_id: str,

    contact: schemas.ContactUpdate,

    current_user=Depends(
        require_role(
            ["Admin", "Employee"]
        )
    )

):

    success = crud.update_contact(
        contact_id,
        contact
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return {
        "message": "Contact updated successfully"
    }

@router.delete("/{contact_id}")
def delete_contact(

    contact_id: str,

    current_user=Depends(
        require_role(
            ["Admin"]
        )
    )

):

    success = crud.delete_contact(contact_id)

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return {
        "message": "Contact deleted successfully"
    }


@router.get("/search/")
def search_contacts(

    name: str = None,
    company: str = None,
    city: str = None,

    current_user=Depends(
        require_role(
            ["Admin", "Employee", "Viewer"]
        )
    )

):

    return crud.search_contacts(
        name,
        company,
        city
    )


from typing import Optional


@router.get("/sort/")
def sort_contacts(

    sort_by: str = "first_name",
    order: str = "asc",

    current_user=Depends(
        require_role(
            ["Admin", "Employee", "Viewer"]
        )
    )

):

    return crud.sort_contacts(
        sort_by,
        order
    )


@router.get("/statistics/")
def get_statistics(

    current_user=Depends(
        require_role(
            ["Admin"]
        )
    )

):

    return crud.get_statistics()