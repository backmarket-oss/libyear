.DEFAULT_GOAL := help

.PHONY: init
init: ## Setup the requirements
	$(info --- Setup ---)
	@poetry install

.PHONY: test-unit
test-unit: init ## Run unit test
	$(info --- Run Python unit-test ---)
	@poetry run pytest

.PHONY: install
install: ## Run install
	$(info --- Run Install ---)
	@poetry install --only main

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
