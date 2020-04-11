.PHONY: typecheck
typecheck:
	mypy --ignore-missing-imports streamingbot

.PHONY: lint
lint:
	pylint streamingbot

.PHONY: test-all
test-all: typecheck lint
