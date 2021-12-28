from pydantic import BaseModel


class QuizBase(BaseModel):
    name: str


class QuizCreate(QuizBase):
    pass


class QuizOut(QuizBase):
    id: int

    # TODO: add questions

    class Config:
        orm_mode = True


class QuizUpdate(QuizBase):
    pass
