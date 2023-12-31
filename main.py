import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from routers import logs as LogRouter
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(LogRouter.router, prefix="/logs")
if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)