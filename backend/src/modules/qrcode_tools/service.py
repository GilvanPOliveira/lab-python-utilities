import base64
from io import BytesIO

import qrcode

from src.modules.qrcode_tools.schemas import QrCodeRequest


def generate_qrcode(payload: QrCodeRequest) -> dict[str, str]:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=payload.box_size,
        border=payload.border,
    )

    qr.add_data(payload.data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "image_base64": image_base64,
        "mime_type": "image/png",
        "filename": "qrcode.png",
    }
