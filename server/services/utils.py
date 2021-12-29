from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from db.user import User


def get_user_by_email(db: Session, email: str):
    """Gets the user by email.

    Args:
        email (str)

    Raises:
        NoResultFound: if the user does not exist.

    Returns:
        (User): db user's model.
    """

    return db.query(User).filter(User.email == email).one()


def create_and_get_user_by_email(db: Session, email: str):
    """Creates and returns a user by email, if he already exists
    it just returns him.

    Args:
        email (str)

    Returns:
        (User): db user's model.
    """

    try:
        user = db.query(User).filter(User.email == email).one()
        return user
    except NoResultFound:
        new_user = User(email=email)
        db.add(new_user)
        db.commit()
        return new_user
