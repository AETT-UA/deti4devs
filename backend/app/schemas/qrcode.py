from pydantic import BaseModel



class QRCodeRequest(BaseModel):
    msg: str
