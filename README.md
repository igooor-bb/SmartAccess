# SmartAccess

SmartAccess allows you to easily add and manage all your important QR codes, barcodes, bonus cards, and tickets in one convenient location – your Apple Wallet. With just a few taps, you can access and use these items whenever you need them.

Streamline your digital life and stay organized with SmartAccess.

## Troubleshooting

For macOS users, it may be problematic to install `m2crypto`. Hence, use the following steps:

Install OpenSSL and SWIG:

```
brew install openssl
brew install swig
```

Change SWIG and clang environment variables during `pip install` so that `m2crypto` will get all OpenSSL requirements:

```
env LDFLAGS="-L$(brew --prefix openssl)/lib" \
CFLAGS="-I$(brew --prefix openssl)/include" \
SWIG_FEATURES="-cpperraswarn -includeall -I$(brew --prefix openssl)/include" \
pip install m2crypto
```

At this point `m2crypto` is installed, you can continue to explore the project.
