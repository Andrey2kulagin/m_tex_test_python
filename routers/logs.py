from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import Response
from database import get_db
from services import logs as LogsService

router = APIRouter()


@router.post('/', tags=["logs"])
async def create(request: Request   , db: Session = Depends(get_db)):
    
    log_data = await request.json()
    log_message = log_data.get("log")
    return Response(status_code=LogsService.create_log(log_message, db))



@router.get("/", tags=["logs"])
async def get(count: int = None, db: Session = Depends(get_db)):
    log_data = LogsService.get_logs(db, count)
    
    return log_data

