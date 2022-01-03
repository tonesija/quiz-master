from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from db.db import get_db
from pydantic_models.question import QuestionOut
from db.question import Question
from db.quiz import Quiz
from pydantic_models.quiz import QuizOut


router = APIRouter(tags=["Public"])


@router.get(
    "/questions",
    response_model=List[QuestionOut],
)
async def list_questions(
    offset: int = 0,
    limit: int = 100,
    q: str = "",
    db: Session = Depends(get_db),
):
    """List public questions."""

    questions = (
        db.query(Question)
        .filter(Question.public == True)
        .filter(Question.outer_text.like(f"%{q}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return questions


@router.get(
    "/questions/count",
    response_model=int,
)
async def count_questions(
    q: str = "",
    db: Session = Depends(get_db),
):
    """Count public questions."""

    count = (
        db.query(Question)
        .filter(Question.public == True)
        .filter(Question.outer_text.like(f"%{q}%"))
        .count()
    )

    return count


@router.get(
    "/quizzes",
    response_model=List[QuizOut],
)
async def list_quizes(
    offset: int = 0,
    limit: int = 100,
    q: str = "",
    db: Session = Depends(get_db),
):
    """List public quizzes."""

    quizes = (
        db.query(Quiz)
        .filter(Quiz.public == True)
        .filter(Quiz.name.like(f"%{q}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return quizes


@router.get(
    "/quizzes/count",
    response_model=int,
)
async def count_quizes(
    q: str = "",
    db: Session = Depends(get_db),
):
    """Count public quizzes."""

    count = (
        db.query(Quiz)
        .filter(Quiz.public == True)
        .filter(Quiz.name.like(f"%{q}%"))
        .count()
    )

    return count


@router.get(
    "/quizzes/{quiz_id}",
    response_model=QuizOut,
)
async def get_public_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    """Get public quiz."""

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id).filter(Quiz.public == True).one()
        )
        return quiz_db
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")


@router.get(
    "/quizzes/{quiz_id}/questions",
    response_model=List[QuestionOut],
)
async def list_public_quiz_questions(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    """List public quizzes questions."""

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id).filter(Quiz.public == True).one()
        )
        return quiz_db.questions
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")
