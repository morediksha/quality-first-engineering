#!/usr/bin/env bash

# Quick Start Setup Script for Jenkins Pipeline with Playwright
# This script sets up the environment and prepares for testing

set -e

echo "======================================"
echo "Jenkins Pipeline - Quick Start Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo -e "${BLUE}Step 1: Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python3 not found. Please install Python 3.7+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Step 2: Create virtual environment
echo -e "${BLUE}Step 2: Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Step 3: Activate virtual environment
echo -e "${BLUE}Step 3: Activating virtual environment...${NC}"
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 4: Install dependencies
echo -e "${BLUE}Step 4: Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 5: Install Playwright browsers
echo -e "${BLUE}Step 5: Installing Playwright browsers...${NC}"
playwright install chromium
echo -e "${GREEN}✓ Playwright browsers installed${NC}"
echo ""

# Step 6: Verify test discovery
echo -e "${BLUE}Step 6: Verifying test discovery...${NC}"
TEST_COUNT=$(pytest tests --collect-only -q | tail -1 | grep -oE '[0-9]+' | head -1 || echo "0")
echo -e "${GREEN}✓ Found ${TEST_COUNT} tests${NC}"
echo ""

# Step 7: Check squad_urls.txt
echo -e "${BLUE}Step 7: Checking squad URLs file...${NC}"
if [ ! -f "squad_urls.txt" ]; then
    echo -e "${YELLOW}squad_urls.txt not found. Creating template...${NC}"
    cat > squad_urls.txt << 'EOF'
# Squad Account URLs for Testing
# Add your newly created account URLs here, one per line
# Example format: https://squad-dev.example.com/account/12345
EOF
    echo -e "${GREEN}✓ Template created${NC}"
    echo -e "${YELLOW}  ⚠ Please update squad_urls.txt with your account URLs${NC}"
else
    URL_COUNT=$(grep -c -v '^#' squad_urls.txt || echo "0")
    if [ "${URL_COUNT}" -gt 0 ]; then
        echo -e "${GREEN}✓ squad_urls.txt found with ${URL_COUNT} account(s)${NC}"
    else
        echo -e "${YELLOW}⚠ squad_urls.txt is empty. Please add account URLs${NC}"
    fi
fi
echo ""

# Step 8: Summary
echo -e "${BLUE}======================================"
echo -e "Setup Complete!"
echo -e "=====================================${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. Update squad_urls.txt with your account URLs"
echo "2. Run smoke tests locally: pytest tests/smoke -v"
echo "3. Run regression tests locally: pytest tests/regression -v"
echo "4. Run all tests: pytest tests -v"
echo "5. Generate Allure report: allure generate allure-results -o allure-reports"
echo "6. View report: allure open allure-reports"
echo ""
echo -e "${BLUE}To run Jenkins pipeline:${NC}"
echo "1. Set up Jenkins job with Jenkinsfile"
echo "2. Build with parameters (BRANCH, TESTS_PATH, SQUAD_URL_FILE)"
echo ""
echo -e "${YELLOW}Virtual environment is active. To deactivate: deactivate${NC}"
echo ""
