#!/bin/bash
echo ""
echo "Creating Virtual Environment"
python3 -m venv env

echo "Installing Prerequisites"
env/bin/pip install -r requirements.txt
