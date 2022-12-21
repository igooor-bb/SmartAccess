from fastapi import FastAPI, File, Form, HTTPException, responses
from fastapi.staticfiles import StaticFiles
import uvicorn
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from passbook.models import Pass, Barcode, StoreCard, BarcodeFormat
import tempfile
import io
import os

app = FastAPI()

config = {
    'wwdr': os.getenv('WWDR_PEM', './certs/wwdr.pem'),
    'cert': os.getenv('CERT_PEM', './certs/certificate.pem'),
    'key': os.getenv('KEY_PEM', './certs/key.pem'),
    'pass': os.getenv('KEY_PEM_PASS'),
    'port': os.getenv('PORT', '8000')
}
assert config['pass'] is not None, "Cannot load KEY_PEM_PASS env"


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
    passfile.create(config['cert'], config['key'],
                    config['wwdr'], config['pass'], file.name)
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


app.mount("/", StaticFiles(directory="./static", html=True), name="static")


def run_dev():
    uvicorn.run("espq.main:app", port=int(
        config['port']), host='0.0.0.0', reload=True)


def run_prod():
    uvicorn.run("espq.main:app", port=int(
        config['port']), host='0.0.0.0', reload=False)
