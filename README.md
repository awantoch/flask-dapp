# Experimental Flask Dapp

Setup the dev environment with:

```bash
python -m venv venv
. venv/bin/activate
make install
```

Run Ganache to spawn a local chain, then deploy the contracts with:

`make deploy`

The Flask entrypoint is src/main.py and the frontend starts at templates/index.html

Setup .env and Makefile for deployment/provisioning.
