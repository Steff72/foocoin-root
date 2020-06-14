**FooCoin - CS50W Final Project**

activate venv: source foocoin-env/bin/activate

run server: python3 -m backend.app

run peer server: export PEER=True && python3 -m backend.app

run server with data seed: export SEED=True && python3 -m backend.app

run frontend: in frontend directory: npm start

update react part: npm run build, put static folder from build into backend/app folder and index.html into templates folder
then run only backend and visit '/' for the app to run

see package.json in /frontend for installed node dependencies
see requirements.txt for installed python modules