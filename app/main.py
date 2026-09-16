from fastapi import FastAPI

from routes import ask



app = FastAPI()

app.include_router(ask.router)

@app.get("/")
async def display():
    return {"message":"I am Rocky!"}





