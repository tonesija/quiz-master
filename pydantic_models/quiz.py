from typing import List, Optional
from pydantic import BaseModel

from pydantic_models.question import QuestionOut


class QuizBase(BaseModel):
    name: str
    public: Optional[bool]


class QuizCreate(QuizBase):
    pass


class QuizOut(QuizBase):
    id: int
    questions: List[QuestionOut] = []

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    name: Optional[str]
    public: Optional[bool]
