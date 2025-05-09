write how to add .evn file


-how to run the app locally

cd to the project directory /it_is_five_pm_somewhere
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn backend.app.main:app --reload

-how to run the app using docker

cd to the project directory /it_is_five_pm_somewhere
docker build -f backend/Dockerfile -t my-fastapi-app .
docker run -p 8000:8000 --env-file backend/.env my-fastapi-app


-run tests locally

cd to the project directory /it_is_five_pm_somewhere
PYTHONPATH=$(pwd)/backend pytest backend/tests/integration_test.py -v

- how to run tests using docker

cd to the project directory /it_is_five_pm_somewhere
docker-compose up --build test --abort-on-container-exit --exit-code-from test
docker-compose down
