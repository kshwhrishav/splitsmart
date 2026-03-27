from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupMemberResponse(BaseModel):
    user_id: str
    role: str
    email: str | None = None
    name: str | None = None


class GroupResponse(BaseModel):
    id: str
    name: str
    created_by: str


class GroupDetailResponse(BaseModel):
    id: str
    name: str
    created_by: str
    members: list[GroupMemberResponse]