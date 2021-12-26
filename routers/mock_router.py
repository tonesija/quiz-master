from fastapi import APIRouter, Depends
from auth import authenticate

router = APIRouter(prefix="/test", tags=["mock"])


@router.get("/public")
async def read_public():
    return "Public data"


@router.get("/private")
async def read_private(auth=Depends(authenticate)):
    return "Private data"
