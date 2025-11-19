# Airlines Flight Data ETL Project

## 📋 Project Overview

This project implements a complete **ETL (Extract, Transform, Load)** pipeline that processes airlines flight data and converts prices from **Indian Rupees (INR)** to **US Dollars (USD)**.

### What is ETL?

- **Extract**: Read data from the source (CSV file)
- **Transform**: Clean, process, and convert the data (currency conversion)
- **Load**: Save the transformed data to a destination (new CSV file)

---

## 📁 Project Structure

```
ETL Project/
├── airlines_flights_data.csv          # Original data (300K+ records)
├── etl_pipeline.py                    # Main ETL script (production)
├── etl_demo.ipynb                     # Interactive Jupyter notebook
├── visualize_results.py               # Results visualization script
├── run_etl.sh                         # Bash runner script
├── requirements.txt                   # Python dependencies
├── README.md                          # Detailed documentation
├── QUICKSTART.md                      # Quick start guide
└── PROJECT_OVERVIEW.md                # This file
```

### Generated Output Files

After running the ETL pipeline:

```
├── airlines_flights_data_usd.csv      # Transformed data with USD prices
├── airlines_flights_data_usd_summary.txt  # Summary report
└── etl_results_visualization.png      # Charts and graphs
```

---

## 🚀 How to Use

### Method 1: Quick Run (Recommended)

```bash
# Install dependencies
pip install pandas requests

# Run the ETL pipeline
python etl_pipeline.py

# (Optional) Visualize results
pip install matplotlib seaborn
python visualize_results.py
```

### Method 2: Interactive Exploration

```bash
# Install dependencies
pip install pandas requests matplotlib seaborn

# Open Jupyter notebook
jupyter notebook etl_demo.ipynb
```

### Method 3: Bash Script

```bash
chmod +x run_etl.sh
./run_etl.sh
```

---

## 🔄 ETL Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        EXTRACT                              │
│  • Read airlines_flights_data.csv                          │
│  • Load 300,153 flight records                             │
│  • Validate data structure                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                       TRANSFORM                             │
│  • Fetch current INR → USD exchange rate                   │
│  • Convert all prices from INR to USD                      │
│  • Add metadata columns:                                   │
│    - price_inr (original)                                  │
│    - price_usd (converted)                                 │
│    - currency (USD)                                        │
│    - exchange_rate_used                                    │
│    - conversion_date                                       │
│  • Perform data quality checks                             │
│  • Generate statistics                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                         LOAD                                │
│  • Save transformed data to CSV                            │
│  • Generate summary report                                 │
│  • Log completion status                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Schema

### Input Data (Original)

| Column | Type | Description |
|--------|------|-------------|
| index | int | Record index |
| airline | string | Airline name |
| flight | string | Flight number |
| source_city | string | Departure city |
| departure_time | string | Time of departure |
| stops | string | Number of stops |
| arrival_time | string | Time of arrival |
| destination_city | string | Arrival city |
| class | string | Ticket class (Economy/Business) |
| duration | float | Flight duration in hours |
| days_left | int | Days until departure |
| **price** | **int** | **Price in INR** |

### Output Data (Transformed)

All original columns PLUS:

| Column | Type | Description |
|--------|------|-------------|
| **price_inr** | **int** | **Original price in Indian Rupees** |
| **price_usd** | **float** | **Converted price in US Dollars** |
| **currency** | **string** | **Currency code (USD)** |
| **exchange_rate_used** | **float** | **Exchange rate applied** |
| **conversion_date** | **string** | **Date of conversion** |

---

## 💡 Key Features

### 1. Real-Time Exchange Rates
- Fetches current INR → USD rates from exchangerate-api.com
- Automatic fallback to default rate if API unavailable
- Transparent rate tracking in output data

### 2. Data Quality Checks
- Detects missing values
- Identifies anomalies (negative prices, etc.)
- Logs warnings for data issues

### 3. Comprehensive Logging
- Detailed execution logs
- Progress tracking
- Error handling and reporting

### 4. Statistical Analysis
- Price statistics (min, max, mean, median)
- Comparison between INR and USD
- Breakdown by airline, class, route, etc.

### 5. Visualization
- Price distribution charts
- Airline comparison graphs
- Route analysis
- Class and stops insights

---

## 📈 Sample Results

### Price Statistics

**Original Prices (INR):**
- Minimum: ₹5,949
- Maximum: ₹99,999
- Average: ₹11,897
- Median: ₹8,500

**Converted Prices (USD):**
- Minimum: $71.39
- Maximum: $1,199.99
- Average: $142.76
- Median: $102.00

*(Based on exchange rate: 1 INR = $0.012 USD)*

---

## 🛠️ Technical Details

### Dependencies

- **pandas**: Data manipulation and analysis
- **requests**: HTTP requests for exchange rate API
- **matplotlib**: Data visualization (optional)
- **seaborn**: Statistical visualizations (optional)

### Python Version

- Python 3.7+

### Performance

- Processes 300,000+ records in seconds
- Memory-efficient pandas operations
- Optimized for large datasets

---

## 📝 Use Cases

This ETL pipeline is perfect for:

1. **Data Analysis**: Convert prices for international comparison
2. **Business Intelligence**: Analyze flight pricing trends
3. **Financial Reporting**: Standardize currency for reports
4. **Academic Projects**: Learn ETL concepts with real data
5. **Price Comparison**: Compare airlines in a common currency

---

## 🔧 Customization

### Change Exchange Rate Source

Edit `etl_pipeline.py`:

```python
# Use a different API
response = requests.get('YOUR_API_URL')
```

### Add Custom Transformations

Add your logic in the `transform()` method:

```python
def transform(self):
    # Existing transformations...
    
    # Add your custom transformation
    self.data['price_per_hour'] = self.data['price_usd'] / self.data['duration']
```

### Filter Data

Add filtering before transformation:

```python
# Only process Economy class
self.data = self.data[self.data['class'] == 'Economy']
```

---

## 📚 Learning Resources

### ETL Concepts
- Extract: Reading data from sources
- Transform: Data cleaning, conversion, enrichment
- Load: Writing data to destinations

### Tools & Libraries
- **Pandas**: Data manipulation library
- **Requests**: HTTP library for API calls
- **Logging**: Python's built-in logging module

### Best Practices
- Data validation at each stage
- Error handling and logging
- Metadata tracking (exchange rates, dates)
- Summary reports for auditing

---

## 🎯 Next Steps

After running the basic ETL pipeline, you can:

1. **Analyze the Results**
   ```bash
   python visualize_results.py
   ```

2. **Explore in Jupyter**
   ```bash
   jupyter notebook etl_demo.ipynb
   ```

3. **Customize the Pipeline**
   - Add more transformations
   - Connect to databases
   - Schedule automated runs

4. **Extend the Project**
   - Add more currency conversions
   - Include historical exchange rates
   - Create a web dashboard
   - Build an API endpoint

---

## 🤝 Support

For questions or issues:

1. Check `QUICKSTART.md` for common problems
2. Review `README.md` for detailed documentation
3. Run the Jupyter notebook for interactive examples

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🎓 Educational Value

This project demonstrates:

- ✅ ETL pipeline design and implementation
- ✅ Data transformation and currency conversion
- ✅ API integration for real-time data
- ✅ Error handling and logging
- ✅ Data quality checks
- ✅ Statistical analysis
- ✅ Data visualization
- ✅ Production-ready code structure

Perfect for learning data engineering concepts!

---

**Created**: November 2024  
**Dataset**: Airlines Flight Data (300K+ records)  
**Purpose**: Educational ETL Pipeline with Currency Conversion

