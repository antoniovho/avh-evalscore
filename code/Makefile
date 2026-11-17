.PHONY: test coverage format lint-fix lint verify integration clean

test:
	uv run pytest -v --junitxml=nosetests.xml

coverage:
	uv run pytest --cov=. --cov-report=term-missing --cov-report=xml:coverage.xml

test-coverage:
	uv run pytest -v \
		--cov=. \
		--cov-report=term-missing \
		--cov-report=xml:coverage.xml \
		--junitxml=nosetests.xml

format:
	uv run ruff format .

lint-fix:
	uv run ruff check --fix .

lint:
	uv run ruff format --check .
	uv run ruff check .

verify: lint test

super-verify: format lint-fix lint test-coverage

integration:
	uv run pytest tests/integration/ -v --tb=short

mutation:
	uv run mutmut run

sonar:
	@if [ -f .env ]; then set -a; . ./.env; set +a; fi; \
	test -n "$$SONAR_TOKEN" || (echo "SONAR_TOKEN no está definido"; exit 1); \
	uv run pysonar

ci: clean super-verify mutation sonar

clean:
	@find . -type f \( -name "coverage.xml" -o -name "nosetests.xml" -o -name ".coverage" \) -delete
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
