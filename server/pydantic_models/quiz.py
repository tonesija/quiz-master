from typing import Optional
from pydantic import BaseModel


class QuizBase(BaseModel):
    name: str
    public: Optional[bool]


class QuizCreate(QuizBase):
    pass


class QuizOut(QuizBase):
    id: int

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    name: Optional[str]
    public: Optional[bool]
