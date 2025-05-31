.PHONY: run clean

# Default target
all: run

# Run the server in development mode with auto-reload
run:
	uv run uvicorn src.main:app --reload

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +

# Help target
help:
	@echo "Available targets:"
	@echo "  run    - Start the server in development mode with auto-reload"
	@echo "  clean  - Remove Python cache files and build artifacts"
	@echo "  help   - Show this help message" 