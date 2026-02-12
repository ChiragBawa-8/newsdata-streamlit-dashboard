#!/bin/bash

echo "========================================"
echo "NewsData.io Dashboard - Setup Script"
echo "========================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

python3 --version
echo ""

echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the dashboard, use:"
echo "   streamlit run app.py"
echo ""
echo "Or simply run: ./run.sh"
echo ""
