# Airlines Flight Data ETL Pipeline

This ETL (Extract, Transform, Load) pipeline processes airlines flight data and converts prices from Indian Rupees (INR) to US Dollars (USD).

## Features

- **Extract**: Reads flight data from CSV file
- **Transform**: 
  - Converts prices from INR to USD using real-time exchange rates
  - Adds metadata columns (original price, converted price, exchange rate, conversion date)
  - Performs data quality checks
  - Generates statistics
- **Load**: 
  - Saves transformed data to a new CSV file
  - Creates a detailed summary report

## 📁 Project Structure

```
📦 airlines-ETL-pipeline/
├── 📓 etl_demo.ipynb          # Interactive Jupyter notebook
├── 📄 README.md               # This file
├── 📄 requirements.txt        # Python dependencies
├── 📂 src/                    # Source code
│   ├── etl_pipeline.py        # Main ETL script
│   ├── visualize_results.py   # Visualization script
│   ├── test_etl.py            # Test suite
│   └── run_etl.sh             # Bash runner
└── 📂 docs/                   # Documentation
    ├── QUICKSTART.md
    ├── PROJECT_OVERVIEW.md
    ├── KAGGLE_SETUP.md
    └── ...more guides
```

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Data Source

You can load data in two ways:

### Option 1: Kaggle API (Recommended)
```bash
python etl_pipeline.py --kaggle
```
This automatically downloads the latest data from Kaggle's airlines-flights-data dataset.

### Option 2: Local File
Place `airlines_flights_data.csv` in the project directory and run:
```bash
python etl_pipeline.py
```

## Usage

### Basic Usage with Kaggle API

Simply run the ETL pipeline with the `--kaggle` flag:

```bash
python src/etl_pipeline.py --kaggle
```

This will:
- Fetch data from Kaggle (rohitgrewal/airlines-flights-data)
- Convert prices from INR to USD using current exchange rates
- Output to `airlines_flights_data_usd.csv`
- Generate a summary report in `airlines_flights_data_usd_summary.txt`

### Basic Usage with Local File

```bash
python src/etl_pipeline.py
```

This will:
- Read from `airlines_flights_data.csv`
- Convert prices from INR to USD using current exchange rates
- Output to `airlines_flights_data_usd.csv`
- Generate a summary report in `airlines_flights_data_usd_summary.txt`

### Advanced Usage

You can also use the ETL pipeline programmatically in your own scripts:

```python
from etl_pipeline import FlightDataETL

# Use with Kaggle API
etl = FlightDataETL(
    output_file='airlines_flights_data_usd.csv',
    use_kaggle=True
)
etl.run()

# Use with custom file paths
etl = FlightDataETL(
    input_file='your_input.csv',
    output_file='your_output.csv'
)
etl.run()

# Use with a fixed exchange rate (if you don't want to fetch live rates)
etl = FlightDataETL(
    input_file='airlines_flights_data.csv',
    output_file='airlines_flights_data_usd.csv',
    exchange_rate=0.012  # 1 INR = $0.012 USD
)
etl.run()
```

## Output

The pipeline generates two files:

1. **Transformed Data CSV**: Contains all original columns plus:
   - `price_inr`: Original price in Indian Rupees
   - `price_usd`: Converted price in US Dollars
   - `currency`: Currency code (USD)
   - `exchange_rate_used`: The exchange rate used for conversion
   - `conversion_date`: Date of conversion

2. **Summary Report**: A text file containing:
   - Execution details
   - Exchange rate information
   - Price statistics (min, max, average, median)
   - Data quality metrics

## Exchange Rate

The pipeline automatically fetches the current INR to USD exchange rate from a free API (exchangerate-api.com). If the API is unavailable, it falls back to a default rate.

## Data Quality

The pipeline performs automatic data quality checks:
- Detects missing values
- Identifies negative prices
- Logs warnings for data issues

## Example Output

```
2024-11-13 10:30:15 - INFO - Starting ETL pipeline...
2024-11-13 10:30:15 - INFO - Extracting data from airlines_flights_data.csv...
2024-11-13 10:30:16 - INFO - Successfully extracted 300153 records
2024-11-13 10:30:16 - INFO - Transforming data...
2024-11-13 10:30:16 - INFO - Current exchange rate: 1 INR = $0.0119 USD
2024-11-13 10:30:17 - INFO - Price statistics (USD):
2024-11-13 10:30:17 - INFO -   Min: $70.85
2024-11-13 10:30:17 - INFO -   Max: $1190.48
2024-11-13 10:30:17 - INFO -   Mean: $142.56
2024-11-13 10:30:17 - INFO - Loading data to airlines_flights_data_usd.csv...
2024-11-13 10:30:18 - INFO - ETL pipeline completed successfully!
```

## License

This project is open source and available for educational purposes.
