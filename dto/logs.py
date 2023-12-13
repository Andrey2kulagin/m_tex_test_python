from pydantic import BaseModel, UUID4, HttpUrl, ValidationError
from datetime import datetime


class LogDetail(BaseModel):
    ip: str
    method: str
    uri: HttpUrl
    status_code: int

    @classmethod
    def create(cls, ip: str, method: str, uri: HttpUrl, status_code: int):
        return cls(ip=ip, method=method, uri=uri, status_code=status_code)
    @classmethod
    def parse_from_string(cls, log_string: str):
        try:
            ip, method, status, uri = log_string.split()
            print(status)
            return cls(ip=ip, method=method, status_code=int(status), uri=uri)
        except ValueError as e:
            raise ValidationError(f"Invalid log: {e}")


class Log(BaseModel):
    id: int
    created: datetime
    log: LogDetail
