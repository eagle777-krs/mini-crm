run:
	FLASK_APP=run.py FLASK_ENV=development flask run

db-init:
	python3 create_tables.py

migrate:
	flask db migrate -m "init"

upgrade:
	flask db upgrade