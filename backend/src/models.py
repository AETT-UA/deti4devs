from pydantic import BaseModel



## QRCode API

class QRCodeRequest(BaseModel):
    msg: str
