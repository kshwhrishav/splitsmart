from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User
from app.schemas.group import GroupCreate


def create_group(db: Session, current_user: User, payload: GroupCreate) -> Group:
    group = Group(
        name=payload.name,
        created_by=current_user.id,
    )
    db.add(group)
    db.flush()

    membership = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        role="owner",
    )
    db.add(membership)
    db.commit()
    db.refresh(group)
    return group


def list_groups_for_user(db: Session, user_id: str) -> list[Group]:
    return (
        db.query(Group)
        .join(GroupMember, GroupMember.group_id == Group.id)
        .filter(GroupMember.user_id == user_id)
        .order_by(Group.created_at.desc())
        .all()
    )


def get_group_for_user(db: Session, group_id: str, user_id: str) -> Group:
    group = (
        db.query(Group)
        .options(
            joinedload(Group.memberships).joinedload(GroupMember.user)
        )
        .join(GroupMember, GroupMember.group_id == Group.id)
        .filter(Group.id == group_id, GroupMember.user_id == user_id)
        .first()
    )

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group