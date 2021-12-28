from typing import List, Optional
from pydantic import BaseModel

from pydantic_models.subquestion import SubuestionOut


class QuestionBase(BaseModel):
    outer_text: Optional[str]
    questions_per_slide: int
    public: Optional[bool]
    img_url: Optional[str]


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(QuestionBase):
    id: int

    subquestions: List[SubuestionOut] = []

    class Config:
        orm_mode = True


class QuestionUpdate(BaseModel):
    outer_text: Optional[str]
    questions_per_slide: Optional[int]
    public: Optional[bool]
    img_url: Optional[str]
