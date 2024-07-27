from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from . import models
import qrcode
import io

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}



## QRCode API

from .qrvalidation import encodeQr, decodeQr

@app.post("/qrcode/encode")
async def qrcode_encode_endpoint(data: models.QRCodeRequest):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    # TODO: Use auth to validate user
    
    msg = data.msg

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(encodeQr(msg))
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")
    
@app.post("/qrcode/decode")
async def qrcode_decode_endpoint(data: models.QRCodeRequest):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    msg = data.msg

    userId = decodeQr(msg)

    if userId is None:
        raise HTTPException(status_code=400, detail="Invalid QR code")

    return {"msg": userId}
