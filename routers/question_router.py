from typing import List
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from auth import get_and_create_user
from db.db import get_db
from pydantic_models.question import QuestionCreate, QuestionOut, QuestionUpdate
from db.question import Question
from db.user import User


router = APIRouter(prefix="/my/questions", tags=["Questions"])


@router.get(
    "",
    response_model=List[QuestionOut],
)
async def list_owned(
    offset: int = 0,
    limit: int = 100,
    q: str = "",
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """List current user's owned questions."""

    questions = (
        db.query(Question)
        .filter(Question.user_id == user.id)
        .filter(Question.outer_text.like(f"%{q}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return questions


@router.get(
    "/{question_id}",
    response_model=QuestionOut,
    responses={status.HTTP_404_NOT_FOUND: {}},
)
async def get_question(
    question_id: int,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Get the specific current user's owned question."""

    try:
        question = (
            db.query(Question)
            .filter(Question.user_id == user.id)
            .filter(Question.id == question_id)
            .one()
        )
        return question
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Question not found.")


@router.post("", response_model=QuestionOut)
async def create_question(
    question: QuestionCreate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Creates a question for the authenticated user."""

    question_db = Question(**question.dict())
    question_db.user_id = user.id
    db.add(question_db)
    db.commit()
    return question_db


@router.put("/{question_id}", responses={status.HTTP_404_NOT_FOUND: {}})
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Updates authorized user's question.

    Peforms a partial update. (key value pairs can be excluded)

    Raises:
        HTTPException: 404 if the question is not found.
    """
    try:
        question_query = (
            db.query(Question)
            .filter(Question.user_id == user.id)
            .filter(Question.id == question_id)
        )

        question_query.one()
        question_query.update(question_update.dict(exclude_unset=True))
        db.commit()
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Question not found.")


@router.delete("/{question_id}", responses={status.HTTP_404_NOT_FOUND: {}})
async def delete_question(
    question_id: int,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Deletes authorized user's question.

    Raises:
        HTTPException: 404 if the question is not found.
    """

    try:
        question_db = (
            db.query(Question)
            .filter(Question.user_id == user.id)
            .filter(Question.id == question_id)
            .one()
        )
        db.delete(question_db)
        db.commit()
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Question not found.")
