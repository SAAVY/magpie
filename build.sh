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

echo -e "${BOLD}================== RUNNING LINTER ====================${NC}"
linter_output=$(flake8 . --statistics)
if [ ! -z "$linter_output" ]; then
	echo -e "${BOLD}${RED}FLAKE8 LINTER ERRORS:${NC}";
	echo -e "${BOLD}${YELLOW}$linter_output${NC}"
	exit 1;
fi
echo -e "${BOLD}================== END LINTER ====================${NC}"
echo

echo -e "${BOLD}================== COMPILING FILES ====================${NC}"
find . -name \*.pyc -delete
python -m py_compile client/api.py
echo -e "${BOLD}================== END COMPILE ====================${NC}"
echo

echo -e "${BOLD}================== RUNNING TESTS ====================${NC}"
PYTHONPATH=. nosetests test
code=$?
if [ "$code" != "0" ]; then
	echo -e "${BOLD}${RED}NOT ALL UNIT TESTS PASSED!${NC}";
	exit 1;
fi
echo -e "${BOLD}================== END TESTS ====================${NC}"
echo

echo -e "${BOLD}================== BUILD COMPLETE ====================${NC}"
