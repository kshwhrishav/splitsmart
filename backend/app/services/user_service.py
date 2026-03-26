from sqlalchemy.orm import Session

from app.models.user import User


def get_or_create_user(db: Session, auth_user: dict) -> User:
    auth0_id = auth_user["sub"]

    user = db.query(User).filter(User.auth0_id == auth0_id).first()

    if not user:
        user = User(
            auth0_id=auth0_id,
            email=auth_user.get("email"),
            name=auth_user.get("name"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user