import jwt
from sqlalchemy.orm.session import Session
from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from db.db import get_db
from services.utils import create_and_get_user_by_email

token_auth_scheme = HTTPBearer()


def authenticate(token: str = Depends(token_auth_scheme)):
    """Auth dependency.

    Args:
        token: Bearer token.

    Raises:
        HTTPException: if the authentication is unsuccessful.

    Returns:
        (result): if the autentification was successful.
    """

    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized.")

    return result


def get_email(auth_result=Depends(authenticate)):
    """Auth dependency.

    Args:
        auth_result ([type], optional): auth result gotten from authenticate
        dependency.

    Returns:
        (str): authenticated user's email.
    """

    for key, item in auth_result.items():
        if "/email" in key:
            return item
    return None


def get_and_create_user(db: Session = Depends(get_db), email: str = Depends(get_email)):
    """Auth dependency.

    Args:
        email (str): email from get_email auth dependency.

    Returns:
        (int): authenticated user's id.
    """
    user = create_and_get_user_by_email(db, email)
    return user


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f"https://{settings.DOMAIN}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=settings.ALGORITHMS,
                audience=settings.API_AUDIENCE,
                issuer=settings.ISSUER,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        if self.scopes:
            result = self._check_claims(payload, "scope", str, self.scopes.split(" "))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, "permissions", list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == "scope":
            payload_claim = payload[claim_name].split(" ")

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (
                    f"Insufficient {claim_name} ({value}). You don't have "
                    "access to this resource"
                )
                return result
        return result
