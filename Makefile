run:
	FLASK_APP=run.py FLASK_ENV=development flask run

migrate:
	flask db migrate -m "init"

upgrade:
	flask db upgrade

database:
	python3 create_tables.py

build:
	uv run build