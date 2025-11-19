#!/bin/bash

# ETL Pipeline Runner Script
# This script sets up the environment and runs the ETL pipeline

echo "========================================"
echo "Airlines Flight Data ETL Pipeline"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing pandas..."
    pip3 install pandas
fi

python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing requests..."
    pip3 install requests
fi

echo ""
echo "Running ETL pipeline..."
echo ""

# Run the ETL pipeline
python3 etl_pipeline.py

echo ""
echo "========================================"
echo "ETL Pipeline Execution Complete"
echo "========================================"



