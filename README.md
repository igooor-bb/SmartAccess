# SmartAccess

SmartAccess allows you to easily add and manage all your important QR codes, barcodes, bonus cards, and tickets in one convenient location – your Apple Wallet. With just a few taps, you can access and use these items whenever you need them.

Streamline your digital life and stay organized with SmartAccess.

## Getting started

[Install poetry](https://python-poetry.org/docs/)

```bash
# Use python3.11 project env
poetry env use python3.11

# Install dependencies
poetry install

# Run dev server
poetry run dev
```

## Troubleshooting

For macOS users, it may be problematic to install `m2crypto`. Hence, use the following steps:

Install OpenSSL and SWIG:

```
brew install openssl
brew install swig
```

Change SWIG and clang environment variables during `poetry install` so that `m2crypto` will get all OpenSSL requirements:

```
env LDFLAGS="-L$(brew --prefix openssl)/lib" \
CFLAGS="-I$(brew --prefix openssl)/include" \
SWIG_FEATURES="-cpperraswarn -includeall -I$(brew --prefix openssl)/include" \
poetry install
```

At this point `m2crypto` is installed, you can continue to explore the project.


## Tips

```bash
# Create keys for testing
openssl req -x509 -newkey rsa:4096 -keyout ./certs/key_test.pem -out ./certs/certificate_test.pem -sha256 -days 36500
```