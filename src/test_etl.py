"""
Test Script for ETL Pipeline
Runs a quick test on a sample of the data to verify everything works
"""

import pandas as pd
from etl_pipeline import FlightDataETL
import os


def test_etl_pipeline():
    """Test the ETL pipeline with a small sample"""
    
    print("="*60)
    print("ETL PIPELINE TEST")
    print("="*60)
    
    # Step 1: Create a small test dataset
    print("\n1. Creating test dataset...")
    try:
        df = pd.read_csv('airlines_flights_data.csv', nrows=100)
        test_input = 'test_input.csv'
        df.to_csv(test_input, index=False)
        print(f"   ✓ Created test dataset with {len(df)} records")
    except Exception as e:
        print(f"   ✗ Failed to create test dataset: {e}")
        return False
    
    # Step 2: Run ETL pipeline
    print("\n2. Running ETL pipeline...")
    try:
        etl = FlightDataETL(
            input_file=test_input,
            output_file='test_output.csv',
            exchange_rate=0.012  # Use fixed rate for testing
        )
        success = etl.run()
        if success:
            print("   ✓ ETL pipeline completed successfully")
        else:
            print("   ✗ ETL pipeline failed")
            return False
    except Exception as e:
        print(f"   ✗ ETL pipeline error: {e}")
        return False
    
    # Step 3: Verify output
    print("\n3. Verifying output...")
    try:
        output_df = pd.read_csv('test_output.csv')
        
        # Check record count
        if len(output_df) != len(df):
            print(f"   ✗ Record count mismatch: {len(output_df)} != {len(df)}")
            return False
        print(f"   ✓ Record count correct: {len(output_df)}")
        
        # Check new columns exist
        required_cols = ['price_inr', 'price_usd', 'currency', 'exchange_rate_used', 'conversion_date']
        for col in required_cols:
            if col not in output_df.columns:
                print(f"   ✗ Missing column: {col}")
                return False
        print(f"   ✓ All required columns present")
        
        # Check price conversion
        sample_inr = output_df['price_inr'].iloc[0]
        sample_usd = output_df['price_usd'].iloc[0]
        expected_usd = round(sample_inr * 0.012, 2)
        if abs(sample_usd - expected_usd) > 0.01:
            print(f"   ✗ Price conversion error: {sample_usd} != {expected_usd}")
            return False
        print(f"   ✓ Price conversion accurate")
        
        # Check currency
        if not all(output_df['currency'] == 'USD'):
            print("   ✗ Currency not set to USD")
            return False
        print("   ✓ Currency set correctly")
        
        # Check exchange rate
        if not all(output_df['exchange_rate_used'] == 0.012):
            print("   ✗ Exchange rate not recorded correctly")
            return False
        print("   ✓ Exchange rate recorded correctly")
        
        print("\n   ✓ All verification checks passed!")
        
    except Exception as e:
        print(f"   ✗ Verification error: {e}")
        return False
    
    # Step 4: Display sample results
    print("\n4. Sample results:")
    print("\n" + "-"*60)
    sample = output_df[['airline', 'source_city', 'destination_city', 'price_inr', 'price_usd']].head(5)
    print(sample.to_string(index=False))
    print("-"*60)
    
    # Step 5: Clean up test files
    print("\n5. Cleaning up test files...")
    try:
        os.remove(test_input)
        os.remove('test_output.csv')
        os.remove('test_output_summary.txt')
        print("   ✓ Test files cleaned up")
    except Exception as e:
        print(f"   ⚠ Warning: Could not remove test files: {e}")
    
    return True


def main():
    """Main test execution"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ETL PIPELINE TEST SUITE" + " "*20 + "║")
    print("╚" + "="*58 + "╝")
    print("\nThis will test the ETL pipeline with a small sample of data.")
    print("The full dataset will not be modified.\n")
    
    success = test_etl_pipeline()
    
    print("\n" + "="*60)
    if success:
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nThe ETL pipeline is working correctly.")
        print("You can now run the full pipeline with:")
        print("  python etl_pipeline.py")
    else:
        print("✗ TESTS FAILED")
        print("="*60)
        print("\nPlease check the errors above and try again.")
    print("\n")


if __name__ == "__main__":
    main()



