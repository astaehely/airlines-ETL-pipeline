"""
ETL Pipeline for Airlines Flight Data
Converts prices from Indian Rupees (INR) to US Dollars (USD)
"""

import pandas as pd
import requests
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data_from_kaggle():
    """
    Load data from Kaggle using kagglehub API
    """
    try:
        import kagglehub
        from kagglehub import KaggleDatasetAdapter
        
        logger.info("Loading data from Kaggle...")
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "rohitgrewal/airlines-flights-data",
            "",
        )
        logger.info(f"Successfully loaded {len(df)} records from Kaggle")
        return df
    except ImportError:
        logger.error("kagglehub not installed. Install with: pip install kagglehub")
        return None
    except Exception as e:
        logger.error(f"Failed to load data from Kaggle: {e}")
        return None


class FlightDataETL:
    """ETL Pipeline for flight data with currency conversion"""
    
    def __init__(self, input_file=None, output_file='airlines_flights_data_usd.csv', 
                 exchange_rate=None, use_kaggle=False):
        """
        Initialize ETL pipeline
        
        Args:
            input_file (str): Path to input CSV file (optional if use_kaggle=True)
            output_file (str): Path to output CSV file
            exchange_rate (float): Optional fixed exchange rate (INR to USD)
            use_kaggle (bool): If True, load data from Kaggle API instead of local file
        """
        self.input_file = input_file
        self.output_file = output_file
        self.exchange_rate = exchange_rate
        self.use_kaggle = use_kaggle
        self.data = None
        
    def get_exchange_rate(self):
        """
        Fetch current INR to USD exchange rate from API
        Falls back to a default rate if API fails
        """
        if self.exchange_rate:
            logger.info(f"Using provided exchange rate: 1 INR = ${self.exchange_rate} USD")
            return self.exchange_rate
            
        try:
            logger.info("Fetching current exchange rate from API...")
            # Using exchangerate-api.com (free tier)
            response = requests.get(
                'https://api.exchangerate-api.com/v4/latest/INR',
                timeout=10
            )
            response.raise_for_status()
            rate = response.json()['rates']['USD']
            logger.info(f"Current exchange rate: 1 INR = ${rate} USD")
            return rate
        except Exception as e:
            logger.warning(f"Failed to fetch exchange rate: {e}")
            # Fallback to approximate rate (as of Nov 2024)
            fallback_rate = 0.012
            logger.info(f"Using fallback exchange rate: 1 INR = ${fallback_rate} USD")
            return fallback_rate
    
    def extract(self):
        """
        Extract: Read data from CSV file or Kaggle API
        """
        try:
            if self.use_kaggle:
                logger.info("Extracting data from Kaggle API...")
                self.data = load_data_from_kaggle()
                if self.data is None:
                    return False
            else:
                if not self.input_file:
                    logger.error("No input file specified and use_kaggle=False")
                    return False
                logger.info(f"Extracting data from {self.input_file}...")
                self.data = pd.read_csv(self.input_file)
            
            logger.info(f"Successfully extracted {len(self.data)} records")
            logger.info(f"Columns: {list(self.data.columns)}")
            return True
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            return False
    
    def transform(self):
        """
        Transform: Convert price from INR to USD and perform data cleaning
        """
        logger.info("Transforming data...")
        try:
            # Get exchange rate
            rate = self.get_exchange_rate()
            
            # Convert price from INR to USD
            self.data['price_inr'] = self.data['price']
            self.data['price_usd'] = (self.data['price_inr'] * rate).round(2)
            
            # Add metadata columns
            self.data['currency'] = 'USD'
            self.data['exchange_rate_used'] = rate
            self.data['conversion_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Data quality checks
            logger.info("Performing data quality checks...")
            
            # Check for missing values
            missing_counts = self.data.isnull().sum()
            if missing_counts.any():
                logger.warning(f"Missing values found:\n{missing_counts[missing_counts > 0]}")
            
            # Check for negative prices
            negative_prices = (self.data['price_inr'] < 0).sum()
            if negative_prices > 0:
                logger.warning(f"Found {negative_prices} records with negative prices")
            
            # Summary statistics
            logger.info(f"Price statistics (INR):")
            logger.info(f"  Min: ₹{self.data['price_inr'].min():.2f}")
            logger.info(f"  Max: ₹{self.data['price_inr'].max():.2f}")
            logger.info(f"  Mean: ₹{self.data['price_inr'].mean():.2f}")
            logger.info(f"  Median: ₹{self.data['price_inr'].median():.2f}")
            
            logger.info(f"Price statistics (USD):")
            logger.info(f"  Min: ${self.data['price_usd'].min():.2f}")
            logger.info(f"  Max: ${self.data['price_usd'].max():.2f}")
            logger.info(f"  Mean: ${self.data['price_usd'].mean():.2f}")
            logger.info(f"  Median: ${self.data['price_usd'].median():.2f}")
            
            logger.info("Transformation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to transform data: {e}")
            return False
    
    def load(self):
        """
        Load: Write transformed data to output CSV file
        """
        logger.info(f"Loading data to {self.output_file}...")
        try:
            # Reorder columns to put USD price prominently
            cols = list(self.data.columns)
            # Remove the new columns from their current position
            for col in ['price_inr', 'price_usd', 'currency', 'exchange_rate_used', 'conversion_date']:
                if col in cols:
                    cols.remove(col)
            
            # Insert them after 'price' column
            price_idx = cols.index('price')
            new_cols = (cols[:price_idx+1] + 
                       ['price_inr', 'price_usd', 'currency', 'exchange_rate_used', 'conversion_date'] + 
                       cols[price_idx+1:])
            
            self.data = self.data[new_cols]
            
            # Save to CSV
            self.data.to_csv(self.output_file, index=False)
            logger.info(f"Successfully loaded {len(self.data)} records to {self.output_file}")
            
            # Create a summary report
            self.create_summary_report()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return False
    
    def create_summary_report(self):
        """
        Create a summary report of the ETL process
        """
        report_file = self.output_file.replace('.csv', '_summary.txt')
        
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("ETL PIPELINE SUMMARY REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Input File: {self.input_file}\n")
            f.write(f"Output File: {self.output_file}\n")
            f.write(f"Total Records Processed: {len(self.data)}\n\n")
            
            f.write("-"*60 + "\n")
            f.write("CURRENCY CONVERSION\n")
            f.write("-"*60 + "\n")
            f.write(f"Exchange Rate Used: 1 INR = ${self.data['exchange_rate_used'].iloc[0]} USD\n")
            f.write(f"Conversion Date: {self.data['conversion_date'].iloc[0]}\n\n")
            
            f.write("-"*60 + "\n")
            f.write("PRICE STATISTICS\n")
            f.write("-"*60 + "\n")
            f.write(f"Original Prices (INR):\n")
            f.write(f"  Minimum: ₹{self.data['price_inr'].min():,.2f}\n")
            f.write(f"  Maximum: ₹{self.data['price_inr'].max():,.2f}\n")
            f.write(f"  Average: ₹{self.data['price_inr'].mean():,.2f}\n")
            f.write(f"  Median:  ₹{self.data['price_inr'].median():,.2f}\n\n")
            
            f.write(f"Converted Prices (USD):\n")
            f.write(f"  Minimum: ${self.data['price_usd'].min():,.2f}\n")
            f.write(f"  Maximum: ${self.data['price_usd'].max():,.2f}\n")
            f.write(f"  Average: ${self.data['price_usd'].mean():,.2f}\n")
            f.write(f"  Median:  ${self.data['price_usd'].median():,.2f}\n\n")
            
            f.write("-"*60 + "\n")
            f.write("DATA QUALITY\n")
            f.write("-"*60 + "\n")
            missing = self.data.isnull().sum()
            if missing.any():
                f.write("Missing Values:\n")
                for col, count in missing[missing > 0].items():
                    f.write(f"  {col}: {count}\n")
            else:
                f.write("No missing values detected\n")
            
            f.write("\n" + "="*60 + "\n")
        
        logger.info(f"Summary report created: {report_file}")
    
    def run(self):
        """
        Execute the complete ETL pipeline
        """
        logger.info("Starting ETL pipeline...")
        logger.info("="*60)
        
        # Extract
        if not self.extract():
            logger.error("ETL pipeline failed at extraction stage")
            return False
        
        # Transform
        if not self.transform():
            logger.error("ETL pipeline failed at transformation stage")
            return False
        
        # Load
        if not self.load():
            logger.error("ETL pipeline failed at loading stage")
            return False
        
        logger.info("="*60)
        logger.info("ETL pipeline completed successfully!")
        return True


def main():
    """Main execution function"""
    import sys
    
    # Check if user wants to use Kaggle API
    use_kaggle = '--kaggle' in sys.argv or '-k' in sys.argv
    
    if use_kaggle:
        print("Using Kaggle API to fetch data...")
        print("Note: Make sure you have kagglehub installed: pip install kagglehub")
        print()
        # Initialize and run ETL pipeline with Kaggle
        etl = FlightDataETL(
            output_file='airlines_flights_data_usd.csv',
            use_kaggle=True
        )
    else:
        # Use local file
        input_file = 'airlines_flights_data.csv'
        output_file = 'airlines_flights_data_usd.csv'
        etl = FlightDataETL(input_file, output_file)
    
    success = etl.run()
    
    if success:
        print("\n" + "="*60)
        print("ETL PROCESS COMPLETED SUCCESSFULLY!")
        print("="*60)
        if use_kaggle:
            print(f"✓ Data source: Kaggle API (rohitgrewal/airlines-flights-data)")
        else:
            print(f"✓ Input file:  {etl.input_file}")
        print(f"✓ Output file: {etl.output_file}")
        print(f"✓ Summary:     {etl.output_file.replace('.csv', '_summary.txt')}")
        print("="*60)
        print("\nTip: Use --kaggle or -k flag to load data from Kaggle API")
        print("     python etl_pipeline.py --kaggle")
    else:
        print("\nETL process failed. Check logs for details.")


if __name__ == "__main__":
    main()

