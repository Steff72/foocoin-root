**FooCoin - Rootserver**

activate venv: source foocoin-env/bin/activate

run server: python3 -m backend.app

run peer server: export PEER=True && python3 -m backend.app

run server with data seed: export SEED=True && python3 -m backend.app


see requirements.txt for installed python modules