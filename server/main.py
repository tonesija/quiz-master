from fastapi import FastAPI
import uvicorn
from config import settings

from fastapi.staticfiles import StaticFiles


app = FastAPI()


@app.get("/posts")
async def root():
    return [
        {
            "title": "Title 1",
            "content": "Content 1",
        },
        {
            "title": "Title 2",
            "content": "Content 3",
        },
    ]


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
