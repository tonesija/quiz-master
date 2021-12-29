from typing import Optional
from pydantic import BaseModel


class SubquestionBase(BaseModel):
    text: str
    answer: str
    img_url: Optional[str]


class SubquestionCreate(SubquestionBase):
    pass


class SubuestionOut(SubquestionBase):
    id: int

    class Config:
        orm_mode = True


class SubestionUpdate(BaseModel):
    text: Optional[str]
    answer: Optional[str]
    img_url: Optional[str]
