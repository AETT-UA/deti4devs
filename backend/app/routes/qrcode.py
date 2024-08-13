from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

import io
import qrcode

from app.dependencies import qrvalidation
from app.schemas.qrcode import QRCodeRequest

router = APIRouter(
    prefix="/qrcode",
    tags=["qrcode"],
    responses={404: {"description": "Not found"}}
)

@router.post("/encode")
async def qrcode_encode(data: QRCodeRequest):
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
    qr.add_data(qrvalidation.encode(msg))
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")
    
@router.post("/decode")
async def qrcode_decode(data: QRCodeRequest):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    msg = data.msg

    userId = qrvalidation.decode(msg)

    if userId is None:
        raise HTTPException(status_code=400, detail="Invalid QR code")

    return {"msg": userId}
