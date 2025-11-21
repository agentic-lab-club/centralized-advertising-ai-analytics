FRONTEND_SERVICE=frontend
BACKEND_SERVICE=backend
DB_SERVICE=postgres_db

build:
	@docker compose up --build -d

up:
	@docker compose up -d

logs:
	@docker compose logs -f

down:
	@docker compose down

exec-backend:
	@docker compose exec $(BACKEND_SERVICE) sh

exec-frontend:
	@docker compose exec $(FRONTEND_SERVICE) sh

exec-psql:
	@docker exec -it $(DB_SERVICE) psql -U postgres -d app_db
