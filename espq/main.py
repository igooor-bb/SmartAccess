from fastapi import FastAPI, File, Form, HTTPException, responses
import uvicorn
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from passbook.models import Pass, Barcode, StoreCard, BarcodeFormat
import tempfile
import io
import os

app = FastAPI()

pwd = os.getenv('KEY_CER_PWD')
assert pwd is not None, "Cannot load KEY_CER_PWD env"


def scan_qr(image: bytes):
    image_np = np.asarray(bytearray(image), dtype=np.uint8)
    image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    qrs = decode(image_cv)
    if len(qrs) != 1:
        return None

    return qrs[0].data.decode()


def create_pkpass(title, data):
    passfile = Pass(
        StoreCard(),
        passTypeIdentifier='pass.wallet.glebosotov.azazkamaz',
        organizationName='',
        teamIdentifier='A6AQ53FW7T',
    )

    passfile.logoText = title
    passfile.serialNumber = 'Bebroid'
    passfile.barcode = Barcode(
        format=BarcodeFormat.QR,
        message=data,
        messageEncoding='utf8',
    )

    passfile.addFile('icon.png', open('./assets/icon.png', 'rb'))
    passfile.addFile('logo.png', open('./assets/logo.png', 'rb'))

    file = tempfile.NamedTemporaryFile()
    passfile.create('./certs/certificate.pem', './certs/key.pem',
                    './certs/wwdr.pem', pwd, file.name)
    return io.BytesIO(file.read())


@app.post("/api/submit")
async def submit(image: bytes = File(), title: str = Form()):
    qr = scan_qr(image)

    if qr is None:
        raise HTTPException(400, "Should be exactly one QR")

    file = create_pkpass(title, qr)

    return responses.StreamingResponse(
        file,
        headers={'Content-Disposition': 'attachment; filename="pass.pkpass"'},
    )


def run_dev():
    uvicorn.run("espq.main:app", port=8000, host='0.0.0.0', reload=True)


def run_prod():
    uvicorn.run("espq.main:app", port=8000, host='0.0.0.0', reload=False)
