from models.logs import Log
from sqlalchemy.orm import Session
from dto import logs
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import INET


def create_log(log: str, db: Session):
    
    try:
        data = logs.LogDetail.parse_from_string(log)
        print(data)
        log = Log(ip=str(data.ip), method=data.method, uri=str(data.uri), status_code=data.status_code)
        db.add(log)
        db.commit()
        db.refresh(log)
        return 201
    except Exception as e:
        print(e)
        return 418


def get_logs(db, count: int = 50):
    log_data_list = db.query(Log).order_by(desc(Log.created)).limit(count).all()
    for data in log_data_list:
        print(data.method, type(data.method))
    log_models = [
    logs.Log(
        id=log_data.id,
        created=log_data.created,
        log=logs.LogDetail(
            ip=log_data.ip,
            method=log_data.method,
            uri=log_data.uri,
            status_code=log_data.status_code
        )
    )
    for log_data in log_data_list
    ]
    return log_models

