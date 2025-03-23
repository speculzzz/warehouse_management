all: pytest coverage

.PHONY: pytest
pytest:
	@echo "================"
	@echo "= Start pytest ="
	@echo "================"
	@pytest -vv tests/

.PHONY: coverage
coverage:
	@echo "=================="
	@echo "= Tests coverage ="
	@echo "=================="
	@pytest -s --cov --cov-report html --cov-fail-under 75
