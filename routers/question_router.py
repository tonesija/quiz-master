from typing import List
from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session
from auth import get_and_create_user
from db.db import get_db

from pydantic_models.question import QuestionCreate, QuestionOut
from db.question import Question
from db.quiz import Quiz
from db.user import User


router = APIRouter(prefix="/my", tags=["Questions"])


def create_question(question: QuestionCreate, db: Session, quiz_id: int = None):
    """Creates a question in the db. If the quiz id is specified, the question
    and the quiz are linken.

    Args:
        question (QuestionCreate): question pydantic model.
        db (Session): db session.
        quiz_id (int, optional): Id of a quiz. Defaults to None.
    """

    if quiz_id:
        quiz_db = db.query(Quiz).filter(Quiz, id == quiz_id).one()
        question_db = Question(**question.dict())
        quiz_db.append(question_db)
        db.add(quiz_db)
    else:
        question_db = Question(**question.dict())
        db.add(question_db)
    db.commit()


@router.get("/questions", response_model=List[QuestionOut])
async def list_all(
    user: User = Depends(get_and_create_user), db: Session = Depends(get_db)
):
    """List all current user's questions."""

    questions = db.query(Question).filter(Question.user_id == user.id).all()
    return questions
