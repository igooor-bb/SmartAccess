import espq


def test_scan():
    with open("./assets/test_qr.jpg", "rb") as f:
        scanned = espq.scan_qr(f.read())
    assert scanned == "https://suishenmafront1.sh.gov.cn/smzy/" \
        "fyz/qrcodeDetail?ewmid=8W1lYhwLBh9bZzk8GeZjGLcsvBpvKoB1pPyVd6" \
        "9w%2F4hSLWtxS9cJfLAJL%2BbCoDWmKS9yrOXp749BwAX8DcdBNQ%3D%3D&" \
        "date=1585455744000&from=8&type=3"


def test_create():
    pkpass = espq.create_pkpass("Test", "Test Data")
    assert pkpass is not None
