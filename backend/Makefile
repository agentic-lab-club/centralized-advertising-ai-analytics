depl-build:
	@echo "Building Docker Image to dotpep/flaudlitebackend..."
	
	@docker build -t dotpep/flaudlitebackend .

depl-push:
	@echo "Pushing Docker Image to dotpep/flaudlitebackend..."
	
	@docker push dotpep/flaudlitebackend

run:
	@echo "Server is on running..."

	@fastapi dev .\app\main.py

build:
	@docker compose up --build -d

up:
	@docker compose up -d

logs:
	@docker compose logs -f

down:
	@docker compose down

dc-remove:
	@docker compose down -v
	#@docker-compose down --remove-orphans

dc-exec-app:
	@docker exec -it fastapi_app sh

dc-exec-db:
	@docker exec -it postgres_db psql -U postgres -d app_db
	#@docker exec -it postgres_db sh

test:
	@echo "Testing..."
	@poetry pytest