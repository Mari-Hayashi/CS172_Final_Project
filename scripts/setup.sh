#!/bin/bash
echo ""
echo "Creating Virtual Environment"
python -m venv env

echo "Installing Prerequisites"
env/bin/pip install -r requirements.txt
