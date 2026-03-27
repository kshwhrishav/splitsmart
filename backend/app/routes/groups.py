from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_auth_user
from app.schemas.group import GroupCreate, GroupDetailResponse, GroupMemberResponse, GroupResponse
from app.services.group_service import create_group, get_group_for_user, list_groups_for_user
from app.services.user_service import get_or_create_user

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=GroupResponse)
def create_group_route(
    payload: GroupCreate,
    auth_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    current_user = get_or_create_user(db, auth_user)
    group = create_group(db, current_user, payload)

    return GroupResponse(
        id=group.id,
        name=group.name,
        created_by=group.created_by,
    )


@router.get("", response_model=list[GroupResponse])
def list_groups_route(
    auth_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    current_user = get_or_create_user(db, auth_user)
    groups = list_groups_for_user(db, current_user.id)

    return [
        GroupResponse(
            id=group.id,
            name=group.name,
            created_by=group.created_by,
        )
        for group in groups
    ]


@router.get("/{group_id}", response_model=GroupDetailResponse)
def get_group_route(
    group_id: str,
    auth_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db),
):
    current_user = get_or_create_user(db, auth_user)
    group = get_group_for_user(db, group_id, current_user.id)

    members = [
        GroupMemberResponse(
            user_id=membership.user_id,
            role=membership.role,
            email=membership.user.email,
            name=membership.user.name,
        )
        for membership in group.memberships
    ]

    return GroupDetailResponse(
        id=group.id,
        name=group.name,
        created_by=group.created_by,
        members=members,
    )