#! /bin/bash

# ANSI COLOR CODES
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}================== INSTALLING REQUIREMENTS ====================${NC}"
pip install -r requirements.txt
echo -e "${BOLD}================== END INSTALL REQUIREMENTS ====================${NC}"
