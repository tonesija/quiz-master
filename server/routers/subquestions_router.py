from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from auth import get_and_create_user
from db.db import get_db
from db.question import Question
from db.user import User
from db.subquestion import Subquestion
from pydantic_models.subquestion import (
    SubestionUpdate,
    SubquestionCreate,
    SubuestionOut,
)


router = APIRouter(
    prefix="/my/questions/{question_id}/subquestions", tags=["Subquestions"]
)


@router.post(
    "/", response_model=SubuestionOut, responses={status.HTTP_404_NOT_FOUND: {}}
)
async def create_subquestions(
    question_id: int,
    subquestion: SubquestionCreate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Creates a subquestion and adds it to the authorized user's question.

    Raises:
        HTTPException: 404 if the question was not found.
    """

    try:
        question = (
            db.query(Question)
            .filter(Question.id == question_id)
            .filter(Question.user_id == user.id)
            .one()
        )
        print(question.id, question_id)

        subquestion = Subquestion(**subquestion.dict())
        question.subquestions.append(subquestion)
        db.add(question)
        db.commit()
        return subquestion
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Question not found.")


@router.put("/{subquestion_id}", responses={status.HTTP_404_NOT_FOUND: {}})
async def update_subquestion(
    question_id: int,
    subquestion_id: int,
    subquestion_update: SubestionUpdate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Updates authorized user's subquestion.

    Raises:
        HTTPException: 404 if the question or subquestion is not found.
    """

    try:
        # Trigger NoResultFound if it is not the authorized user's question.
        db.query(Question).filter(Question.user_id == user.id).filter(
            Question.id == question_id
        ).one()

        subquestion_query = db.query(Subquestion).filter(
            Subquestion.id == subquestion_id and Subquestion.question_id == question_id
        )
        subquestion_query.one()
        subquestion_query.update(subquestion_update.dict(exclude_unset=True))
        db.commit()
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Question or subquestion not found."
        )


@router.delete("/{subquestion_id}", responses={status.HTTP_404_NOT_FOUND: {}})
async def delete_subquestion(
    question_id: int,
    subquestion_id: int,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Deletes authorized user's subquestion.

    Raises:
        HTTPException: 404 if the question or subquestion is not found.
    """

    try:
        # Trigger NoResultFound if it is not the authorized user's question.
        db.query(Question).filter(Question.user_id == user.id).filter(
            Question.id == question_id
        ).one()

        subquestion_db = (
            db.query(Subquestion)
            .filter(
                Subquestion.id == subquestion_id
                and Subquestion.question_id == question_id
            )
            .one()
        )
        db.delete(subquestion_db)
        db.commit()
    except NoResultFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Question or subquestion not found."
        )
