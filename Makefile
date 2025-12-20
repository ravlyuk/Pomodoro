.DEFAULT_GOAL := help

run:
	poetry run gunicorn main:app -c infrastructure/gunicorn.conf.py --reload

migrate:
	alembic revision --autogenerate -m "$(m)"

upgrade:
	alembic upgrade head

history:
	alembic history --verbose -r-3:current

reset-db:
    @echo "WARNING: This will delete all data and migrations. Proceed with caution"
    @read -p "Are you sure? [y/N] " -n 1 -r; echo; if [[ $$REPLY =~ ^[Yy]$$ ]]; then rm -f alembic/versions/*.py; docker-compose exec db psql -U postgres -d pomodoro -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"; echo "Database reset complete."; fi


help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'	