lint:
	uv run ruff check --fix .
	uv run ruff format .
	uv run ty check .

test:
	uv run pytest \
		--cov=src \
		--cov-report=term \
		--cov-report=html \
		--cov-report=lcov \
		--tb=short \
		--maxfail=1 \
		--cov-config=.coveragerc \
		--ignore-glob=__init__.py

check:
	make lint
	make test