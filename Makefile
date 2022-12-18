.PHONY: all test clean

requirments:
	pipreqs . --force

black: 
	black -l 120 -t py310 .
	
deps:  ## Install dependencies
	pip install poetry
	poetry install

test: ## Run tests
	poetry run pytest -v .

coverage: ## Run coverage
	poetry run coverage report -m .

doc: 
	pdoc --http localhost:8080 substrate
