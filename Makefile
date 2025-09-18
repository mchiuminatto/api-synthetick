run:
	uvicorn --reload app.main:app

lint:
	flake8 --max-line-length=120 --extend-ignore=E203 app tests

docker-run:
	docker run -p 8000:8000 mchiuminatto/api-synthetick

dk-up:
	docker compose up --build

dk-dn:
	docker compose down

test:
	coverage run -m pytest

cov-report:
	coverage report -m