write how to add .evn file


how to run the app locally

cd to the project directory /it_is_five_pm_somewhere
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload

how to run the app using docker

cd to the project directory /it_is_five_pm_somewhere
docker build -f backend/Dockerfile -t my-fastapi-app .
docker run -p 8000:8000 --env-file backend/.env my-fastapi-app


run tests locally
pytest backend/tests/integration_test.py -v

run tests using docker
docker run --rm -v "$PWD":/app -w /app/backend my-fastapi-app pytest tests/integration_test.py
