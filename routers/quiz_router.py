from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from auth import get_and_create_user
from db.db import get_db
from db.quiz import Quiz
from pydantic_models.quiz import QuizCreate, QuizOut, QuizUpdate
from db.user import User
from db.question import Question
from pydantic_models.group import GroupAddQuestion
from pydantic_models.question import QuestionOut

router = APIRouter(prefix="/my/quizzes", tags=["Quizzes"])


@router.get("", response_model=List[QuizOut])
async def list(
    user: User = Depends(get_and_create_user), db: Session = Depends(get_db)
):
    """List current user's quizzes."""

    quizes = db.query(Quiz).filter(Quiz.user_id == user.id).all()
    return quizes


@router.get(
    "/{quiz_id}", response_model=QuizOut, responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_quiz(
    quiz_id: int,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Return a current user's specific quiz.

    Raises:
        HTTPException: 404 if the quiz is not found.
    """

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id and Quiz.user_id == user.id).one()
        )
        return quiz_db
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")


@router.get(
    "/{quiz_id}/questions",
    response_model=List[QuestionOut],
    responses={status.HTTP_404_NOT_FOUND: {}},
)
async def list_questions(
    quiz_id: int,
    offset: int = 0,
    limit: int = 100,
    q: str = "",
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """List current user's quizzes questions."""

    try:
        quiz_db = (
            db.query(Quiz)
            .filter(Quiz.id == quiz_id and Quiz.users.contains(user))
            .one()
        )
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")

    questions = (
        db.query(Question)
        .filter(Question.quizes.contains(quiz_db))
        .filter(Question.outer_text.like(f"%{q}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return questions


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
    response_model=QuizOut,
)
async def create_quiz(
    quiz: QuizCreate,
    user: User = Depends(get_and_create_user),
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
        quiz_db.user_id = user.id
        db.add(quiz_db)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Quiz name taken."
        )
    return quiz_db


@router.put(
    "/{quiz_id}",
    responses={status.HTTP_404_NOT_FOUND: {}, status.HTTP_409_CONFLICT: {}},
)
async def update_quiz(
    quiz_id: int,
    quiz_update: QuizUpdate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Updates current user's quiz.

    Peforms a partial update. (key value pairs can be excluded)

    Raises:
        HTTPException: 404 if the quiz is not found.
        HTTPException: 409 if the quiz with the same name already exists.
    """

    try:
        quiz_query = db.query(Quiz).filter(
            Quiz.id == quiz_id and Quiz.user_id == user.id
        )
        quiz_query.one()
        quiz_query.update(quiz_update.dict(exclude_unset=True))
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
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Delete current user's quiz.

    Raises:
        HTTPException: 404 if the quiz is not found.
    """

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id and Quiz.user_id == user.id).one()
        )
        db.delete(quiz_db)
        db.commit()
        return
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")


@router.post(
    "/{quiz_id}/add-question",
    responses={status.HTTP_404_NOT_FOUND: {}, status.HTTP_401_UNAUTHORIZED: {}},
)
async def add_question(
    quiz_id: int,
    question_payload: GroupAddQuestion,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Add a question to the current user's quiz.

    Raises:
        HTTPException: 403 if the current user is not the quizes owner.
        HTTPException: 404 if the quiz is not found or if the question is not found.
    """

    try:
        quiz_db = (
            db.query(Quiz).filter(Quiz.id == quiz_id and Quiz.user_id == user.id).one()
        )

        try:
            question_db = (
                db.query(Question)
                .filter(Question.id == question_payload.question_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Question not found.")

        quiz_db.questions.append(question_db)
        db.add(quiz_db)
        db.commit()
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Quiz not found.")
