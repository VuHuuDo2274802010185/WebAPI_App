.PHONY: help install run-api run-ui test docker-build docker-run clean

help:
	@echo "Base.vn Candidate API Wrapper - Available Commands"
	@echo "=================================================="
	@echo "make install       - Install dependencies"
	@echo "make run-api       - Run FastAPI server"
	@echo "make run-ui        - Run Streamlit UI"
	@echo "make test          - Run API tests"
	@echo "make example       - Run example usage script"
	@echo "make docker-build  - Build Docker image"
	@echo "make docker-run    - Run with Docker Compose"
	@echo "make docker-stop   - Stop Docker containers"
	@echo "make clean         - Clean Python cache files"

install:
	pip install -r requirements.txt

run-api:
	python api_server.py

run-ui:
	streamlit run app.py

test:
	python test_api.py

example:
	python example_usage.py

docker-build:
	docker build -t webapi-app .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
