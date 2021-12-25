from fastapi import FastAPI
import uvicorn
from config import settings
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve SPA
app.mount("/", StaticFiles(directory="public/build"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
