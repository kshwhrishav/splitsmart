from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_auth_user
from app.services.user_service import get_or_create_user

router = APIRouter(tags=["users"])


@router.get("/me")
def get_me(
    auth_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    user = get_or_create_user(db, auth_user)
    return {
        "id": user.id,
        "auth0_id": user.auth0_id,
        "email": user.email,
        "name": user.name,
    }