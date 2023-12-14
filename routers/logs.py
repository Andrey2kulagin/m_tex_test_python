from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import Response
from database import get_db
from services import logs as LogsService


router = APIRouter()


@router.post('/', tags=["user"])
async def create(log: str = "", db: Session = Depends(get_db)):
    return Response(status_code=LogsService.create_log(log, db))
    #JSONResponse(status_code=204)


@router.get("/", tags=["user"])
async def get(count: int = None, db: Session = Depends(get_db)):
    log_data = LogsService.get_logs(db, count)
    
    return log_data

