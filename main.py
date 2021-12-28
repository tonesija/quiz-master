from fastapi import FastAPI
import uvicorn
from config import settings

from fastapi.staticfiles import StaticFiles

from routers import quiz_router

app = FastAPI()

# Include routers
app.include_router(quiz_router.router)


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
