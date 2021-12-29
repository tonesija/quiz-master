from fastapi import FastAPI
import uvicorn
from config import settings

from fastapi.staticfiles import StaticFiles

from routers import quiz_router, question_router, groups_router, subquestions_router

app = FastAPI()

# Include routers
app.include_router(quiz_router.router)
app.include_router(question_router.router)
app.include_router(groups_router.router)
app.include_router(subquestions_router.router)


# Serve SPA
if settings.SERVER_MODE != "build":
    app.mount("/", StaticFiles(directory="public/build", html=True))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
