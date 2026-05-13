.PHONY: help train run test

help:
	@echo "train - Train the baseline model"
	@echo "run   - Run the FastAPI application"
	@echo "test  - Run the test suite"

train:
	python -m training.train

run:
	uvicorn app.main:app --reload

test:
	pytest
