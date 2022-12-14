.PHONY: all test clean

requirments:
	pipreqs . --force

deps:  ## Install dependencies
	pip install poetry
	poetry install

test: ## Run tests
	poetry run pytest -v .

coverage: ## Run coverage
	poetry run coverage report -m

doc: 
	pdoc --http localhost:8080 substrate
