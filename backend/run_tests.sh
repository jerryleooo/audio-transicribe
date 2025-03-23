#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up test environment...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ "$1" == "--install" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
    pip install pytest pytest-cov
fi

# Set environment variables for testing
export FLASK_ENV=testing
export TESTING=True
export DATABASE_URL=sqlite:///test.db

# Clean up previous test artifacts
echo -e "${YELLOW}Cleaning up previous test artifacts...${NC}"
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
rm -f .coverage
rm -rf htmlcov

# Run tests with coverage
echo -e "${YELLOW}Running tests with coverage...${NC}"
python -m pytest tests/ -v --cov=app --cov-report=term --cov-report=html

# Check test status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    
    # Display coverage report
    echo -e "${YELLOW}Coverage Report:${NC}"
    coverage report
    
    echo -e "${GREEN}HTML coverage report generated in htmlcov/ directory${NC}"
    echo -e "${GREEN}Open htmlcov/index.html in your browser to view detailed coverage report${NC}"
else
    echo -e "${RED}Tests failed!${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo -e "${GREEN}Test run completed successfully!${NC}" 