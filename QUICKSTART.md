# Quick Start Guide - ETL Pipeline

## What This Does

This ETL pipeline converts flight prices from **Indian Rupees (INR)** to **US Dollars (USD)** in your airlines flight dataset.

## Files Created

1. **`etl_pipeline.py`** - Main ETL script (production-ready)
2. **`etl_demo.ipynb`** - Interactive Jupyter notebook for exploration
3. **`requirements.txt`** - Python dependencies
4. **`run_etl.sh`** - Bash script to run the pipeline

## Quick Start

### Option 1: Run the Python Script (Recommended)

```bash
# Install dependencies
pip install pandas requests

# Run the ETL pipeline
python etl_pipeline.py
```

### Option 2: Use the Bash Script

```bash
# Make the script executable
chmod +x run_etl.sh

# Run it
./run_etl.sh
```

### Option 3: Use the Jupyter Notebook

```bash
# Install additional dependencies for visualization
pip install pandas requests matplotlib seaborn

# Start Jupyter
jupyter notebook etl_demo.ipynb
```

## What You'll Get

After running the ETL pipeline, you'll have:

1. **`airlines_flights_data_usd.csv`** - Your transformed data with prices in USD
2. **`airlines_flights_data_usd_summary.txt`** - A detailed summary report

## Example Output

The transformed CSV will have these new columns:

| Column | Description |
|--------|-------------|
| `price_inr` | Original price in Indian Rupees |
| `price_usd` | Converted price in US Dollars |
| `currency` | Currency code (USD) |
| `exchange_rate_used` | The exchange rate used for conversion |
| `conversion_date` | Date when conversion was performed |

## Sample Data

**Before (Original):**
```
airline,flight,source_city,destination_city,price
SpiceJet,SG-8709,Delhi,Mumbai,5953
```

**After (Transformed):**
```
airline,flight,source_city,destination_city,price,price_inr,price_usd,currency,exchange_rate_used,conversion_date
SpiceJet,SG-8709,Delhi,Mumbai,5953,5953,71.44,USD,0.0120,2024-11-13
```

## Customization

### Use a Fixed Exchange Rate

If you don't want to fetch live rates, you can specify a fixed rate:

```python
from etl_pipeline import FlightDataETL

etl = FlightDataETL(
    input_file='airlines_flights_data.csv',
    output_file='airlines_flights_data_usd.csv',
    exchange_rate=0.012  # Fixed rate: 1 INR = $0.012 USD
)
etl.run()
```

### Process Different Files

```python
from etl_pipeline import FlightDataETL

etl = FlightDataETL(
    input_file='your_custom_input.csv',
    output_file='your_custom_output.csv'
)
etl.run()
```

## Troubleshooting

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install pandas requests
```

### Issue: "Exchange rate API failed"
**Solution:** The pipeline automatically uses a fallback rate. No action needed.

### Issue: "File not found"
**Solution:** Make sure you're in the correct directory
```bash
cd "/Users/aaronstaehely/Documents/Sabermetrics work/ETL Project"
```

## Need Help?

- Check `README.md` for detailed documentation
- Run the Jupyter notebook (`etl_demo.ipynb`) for an interactive walkthrough
- Review the summary report after running the pipeline

## Exchange Rate Information

The pipeline fetches real-time exchange rates from exchangerate-api.com. If the API is unavailable, it uses a fallback rate of approximately 1 INR = $0.012 USD.

Current approximate conversion:
- ₹1,000 INR ≈ $12 USD
- ₹10,000 INR ≈ $120 USD
- ₹100,000 INR ≈ $1,200 USD

