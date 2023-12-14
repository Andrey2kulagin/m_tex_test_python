from pydantic import BaseModel, UUID4, HttpUrl, ValidationError
from datetime import datetime
from ipaddress import IPv4Address
from enum import Enum
class HttpMethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    TRACE = "TRACE"   

class LogDetail(BaseModel):
    ip: IPv4Address
    method: HttpMethodEnum
    uri: HttpUrl
    status_code: int

    @classmethod
    def create(cls, ip: str, method: str, uri: HttpUrl, status_code: int):
        return cls(ip=ip, method=method, uri=uri, status_code=status_code)
    @classmethod
    def parse_from_string(cls, log_string: str):
        try:
            ip, method, uri, status= log_string.split()
            return cls(ip=IPv4Address(ip), method=HttpMethodEnum(method.upper()), status_code=int(status), uri=uri)
        except ValueError as e:
            raise ValidationError(f"Invalid log: {e}")


class Log(BaseModel):
    id: UUID4
    created: datetime
    log: LogDetail

class LogCreate(BaseModel):
    log: str
