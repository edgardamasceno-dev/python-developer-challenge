#!/bin/bash

# Run tests with coverage
echo "Running tests with coverage..."

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run pytest with coverage
python -m pytest

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo "Coverage report saved to htmlcov/index.html"
else
    echo "Tests failed!"
    exit 1
fi