#! /bin/bash

echo "================== INSTALLING REQUIREMENTS ===================="
pip install -r requirements.txt
echo "================== END INSTALL REQUIREMENTS ===================="
echo
echo "================== RUNNING LINTER ===================="
flake8 .
echo "================== END LINTER ===================="
echo
echo "================== BEGIN FLASK SERVER ===================="
python client/api.py
