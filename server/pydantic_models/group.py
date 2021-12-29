from typing import List, Optional
from pydantic import BaseModel

from db.group import Group


class GroupBase(BaseModel):
    name: str
    desc: Optional[str]


class GroupCreate(GroupBase):
    pass


class GroupOut(GroupBase):
    id: int
    users: List[str] = []

    @classmethod
    def from_orm(cls, group_db: Group):
        """Overrides the from_orm class method from pydantic.
        Neccessary to get the user's emails that belong to the group.

        Args:
            group_db (Group): db model of the group.

        Returns:
            (GroupOut): pydantic model.
        """

        emails = [user.email for user in group_db.users]
        return cls(
            id=group_db.id,
            name=group_db.name,
            desc=group_db.desc,
            users=emails,
        )

    class Config:
        orm_mode = True


class GroupUpdate(BaseModel):
    name: Optional[str]
    desc: Optional[str]


class GroupAddMember(BaseModel):
    email: str


class GroupAddQuestion(BaseModel):
    question_id: int
