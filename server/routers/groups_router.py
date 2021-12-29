from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from auth import get_and_create_user
from db.db import get_db
from pydantic_models.group import GroupAddMember, GroupCreate, GroupOut, GroupUpdate
from db.group import Group
from db.user import User
from services.utils import get_user_by_email


router = APIRouter(prefix="/my/groups", tags=["Groups"])


@router.get("/", response_model=List[GroupOut])
async def list(
    user: User = Depends(get_and_create_user), db: Session = Depends(get_db)
):
    """List current user's groups."""

    groups = db.query(Group).filter(Group.users.contains(user)).all()
    return groups


@router.get(
    "/{group_id}}", response_model=GroupOut, responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_group(
    group_id: int,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Return a current user's specific group.

    Raises:
        HTTPException: 404 if the group is not found.
    """

    try:
        group_db = (
            db.query(Group)
            .filter(Group.id == group_id and Group.user_id == user.id)
            .one()
        )
        return group_db
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Group not found.")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {}},
)
async def create_group(
    group: GroupCreate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Create a group.

    Args:
        group (GroupCreate): body payload.

    Raises:
        HTTPException: 409 if the group with the same name already exists.
    """

    try:
        group_db = Group(**group.dict())
        group_db.user_id = user.id
        group_db.users.append(user)
        db.add(group_db)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Group name taken."
        )
    return


@router.put(
    "/{group_id}",
    responses={status.HTTP_404_NOT_FOUND: {}, status.HTTP_409_CONFLICT: {}},
)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Updates current user's group.

    Raises:
        HTTPException: 404 if the group is not found.
        HTTPException: 409 if the group with the same name already exists.
    """

    try:
        group_query = db.query(Group).filter(
            Group.id == group_id and Group.user_id == user.id
        )
        group_query.one()
        group_query.update(group_update.dict(exclude_unset=True))
        db.commit()
        return
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Group not found.")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Group name taken."
        )


@router.delete("/{group_id}", responses={status.HTTP_404_NOT_FOUND: {}})
async def delete_group(
    group_id: int,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Delete current user's group.

    Raises:
        HTTPException: 404 if the group is not found.
    """

    try:
        group_db = (
            db.query(Group)
            .filter(Group.id == group_id and Group.user_id == user.id)
            .one()
        )
        db.delete(group_db)
        db.commit()
        return
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Group not found.")


@router.post(
    "/{group_id}/add-member",
    responses={status.HTTP_404_NOT_FOUND: {}, status.HTTP_401_UNAUTHORIZED: {}},
)
async def add_member(
    group_id: int,
    email_payload: GroupAddMember,
    user: User = Depends(get_and_create_user),
    db: Session = Depends(get_db),
):
    """Add a user to the current user's group.

    Raises:
        HTTPException: 403 if the current user is not the group's owner.
        HTTPException: 404 if the group is not found or if the user is not found.
    """

    try:
        group_db = (
            db.query(Group)
            .filter(Group.id == group_id and Group.user_id == user.id)
            .one()
        )
        if group_db.user_id != user.id:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Only group's owner can add members.",
            )

        try:
            user_db = get_user_by_email(db, email_payload.email)
        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found.")

        group_db.users.append(user_db)
        db.add(group_db)
        db.commit()
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Group not found.")
