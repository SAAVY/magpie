#! /bin/bash

# ANSI COLOR CODES
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}================== CHECK VIRTUAL ENV ====================${NC}"
python -c 'import sys; print sys.real_prefix' 2>/dev/null && INVENV=1 || INVENV=0
if [ $INVENV -eq 0 ]; then
	echo -e "${RED}ERROR: Not in virtual env! Source env by doing . venv/bin/activate${NC}";
	exit 1;
fi

echo -e "${BOLD}================== INSTALLING REQUIREMENTS ====================${NC}"
pip install -r requirements.txt
echo -e "${BOLD}================== END INSTALL REQUIREMENTS ====================${NC}"
