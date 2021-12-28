from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from auth import get_and_create_users_id
from db.db import get_db
from db.quiz import Quiz
from pydantic_models.quiz import QuizCreate, QuizOut, QuizUpdate

router = APIRouter(prefix="/my/quizes", tags=["Quizes"])


@router.get("/", response_model=List[QuizOut])
async def list(
    user_id: int = Depends(get_and_create_users_id), db: Session = Depends(get_db)
):
    """List current user's quizes."""

    quizes = db.query(Quiz).filter(Quiz.user_id == user_id).all()
    return quizes


@router.get(
    "/{quiz_id}}", response_model=QuizOut, responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_quiz(
    quiz_id: int,
    user_id: int = Depends(get_and_create_users_id),
    db: Session = Depends(get_db),
):
    """Return a current user's specific quiz.

    Raises:
        HTTPException: 404 if the quiz is not found.
    """

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id and Quiz.user_id == user_id).one()
        )
        return quiz_db
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
)
async def create_quiz(
    quiz: QuizCreate,
    user_id: int = Depends(get_and_create_users_id),
    db: Session = Depends(get_db),
):
    """Create a quiz.

    Args:
        quiz (QuizCreate): body payload.

    Raises:
        HTTPException: 409 if the quiz with the same name already exists.
    """

    try:
        quiz_db = Quiz(**quiz.dict())
        quiz_db.user_id = user_id
        db.add(quiz_db)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Quiz name taken."
        )
    return


@router.put(
    "/{quiz_id}",
    responses={status.HTTP_404_NOT_FOUND: {}, status.HTTP_409_CONFLICT: {}},
)
async def update_quiz(
    quiz_id: int,
    quiz_update: QuizUpdate,
    user_id: int = Depends(get_and_create_users_id),
    db: Session = Depends(get_db),
):
    """Updates current user's quiz.

    Raises:
        HTTPException: 404 if the quiz is not found.
        HTTPException: 409 if the quiz with the same name already exists.
    """

    try:
        quiz_query = db.query(Quiz).filter(
            Quiz.id == quiz_id and Quiz.user_id == user_id
        )
        quiz_query.one()
        quiz_query.update(quiz_update.dict())
        db.commit()
        return
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Quiz name taken."
        )


@router.delete("/{quiz_id}", responses={status.HTTP_404_NOT_FOUND: {}})
async def delete_quiz(
    quiz_id: int,
    user_id: int = Depends(get_and_create_users_id),
    db: Session = Depends(get_db),
):
    """Delete current user's quit.

    Raises:
        HTTPException: 404 if the quiz is not found.
    """

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id and Quiz.user_id == user_id).one()
        )
        db.delete(quiz_db)
        db.commit()
        return
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")
