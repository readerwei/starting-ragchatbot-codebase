quality:
	black --check ./
	isort --check-only ./
	./.venv/bin/ruff check ./

format:
	black ./
	isort ./

lint:
	./.venv/bin/ruff check . --fix
