"""
Visualization Script for ETL Results
Generates charts and insights from the transformed flight data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)


def load_data(filename='airlines_flights_data_usd.csv'):
    """Load the transformed data"""
    if not Path(filename).exists():
        print(f"Error: {filename} not found!")
        print("Please run the ETL pipeline first: python etl_pipeline.py")
        return None
    
    df = pd.read_csv(filename)
    print(f"✓ Loaded {len(df):,} records from {filename}")
    return df


def create_visualizations(df):
    """Create comprehensive visualizations"""
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(18, 12))
    
    # 1. Price Distribution Comparison (INR vs USD)
    ax1 = plt.subplot(2, 3, 1)
    ax1.hist(df['price_inr'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.axvline(df['price_inr'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: ₹{df["price_inr"].mean():,.0f}')
    ax1.set_xlabel('Price (INR)', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title('Price Distribution - Indian Rupees', fontsize=12, fontweight='bold')
    ax1.legend()
    
    ax2 = plt.subplot(2, 3, 2)
    ax2.hist(df['price_usd'], bins=50, color='green', alpha=0.7, edgecolor='black')
    ax2.axvline(df['price_usd'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Mean: ${df["price_usd"].mean():,.0f}')
    ax2.set_xlabel('Price (USD)', fontsize=11)
    ax2.set_ylabel('Frequency', fontsize=11)
    ax2.set_title('Price Distribution - US Dollars', fontsize=12, fontweight='bold')
    ax2.legend()
    
    # 2. Average Price by Airline
    ax3 = plt.subplot(2, 3, 3)
    airline_avg = df.groupby('airline')['price_usd'].mean().sort_values(ascending=True)
    airline_avg.plot(kind='barh', ax=ax3, color='teal', edgecolor='black')
    ax3.set_xlabel('Average Price (USD)', fontsize=11)
    ax3.set_ylabel('Airline', fontsize=11)
    ax3.set_title('Average Price by Airline', fontsize=12, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    
    # 3. Price by Class
    ax4 = plt.subplot(2, 3, 4)
    class_data = df.groupby('class')['price_usd'].mean().sort_values(ascending=False)
    colors = ['gold', 'silver'][:len(class_data)]
    class_data.plot(kind='bar', ax=ax4, color=colors, edgecolor='black')
    ax4.set_xlabel('Class', fontsize=11)
    ax4.set_ylabel('Average Price (USD)', fontsize=11)
    ax4.set_title('Average Price by Class', fontsize=12, fontweight='bold')
    ax4.tick_params(axis='x', rotation=0)
    ax4.grid(axis='y', alpha=0.3)
    
    # 4. Price by Number of Stops
    ax5 = plt.subplot(2, 3, 5)
    stops_data = df.groupby('stops')['price_usd'].mean().sort_values()
    stops_data.plot(kind='bar', ax=ax5, color='coral', edgecolor='black')
    ax5.set_xlabel('Number of Stops', fontsize=11)
    ax5.set_ylabel('Average Price (USD)', fontsize=11)
    ax5.set_title('Average Price by Number of Stops', fontsize=12, fontweight='bold')
    ax5.tick_params(axis='x', rotation=0)
    ax5.grid(axis='y', alpha=0.3)
    
    # 5. Top Routes by Price
    ax6 = plt.subplot(2, 3, 6)
    df['route'] = df['source_city'] + ' → ' + df['destination_city']
    route_avg = df.groupby('route')['price_usd'].mean().sort_values(ascending=False).head(10)
    route_avg.plot(kind='barh', ax=ax6, color='purple', edgecolor='black')
    ax6.set_xlabel('Average Price (USD)', fontsize=11)
    ax6.set_ylabel('Route', fontsize=11)
    ax6.set_title('Top 10 Most Expensive Routes', fontsize=12, fontweight='bold')
    ax6.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Save the figure
    output_file = 'etl_results_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_file}")
    
    plt.show()


def print_insights(df):
    """Print key insights from the data"""
    print("\n" + "="*70)
    print("KEY INSIGHTS FROM TRANSFORMED DATA")
    print("="*70)
    
    # Overall statistics
    print("\n📊 OVERALL STATISTICS:")
    print(f"   Total flights analyzed: {len(df):,}")
    print(f"   Number of airlines: {df['airline'].nunique()}")
    print(f"   Number of routes: {df['source_city'].nunique() * df['destination_city'].nunique()}")
    print(f"   Date range: {df['days_left'].min()} to {df['days_left'].max()} days before departure")
    
    # Price insights
    print("\n💰 PRICE INSIGHTS (USD):")
    print(f"   Cheapest flight: ${df['price_usd'].min():.2f}")
    print(f"   Most expensive flight: ${df['price_usd'].max():.2f}")
    print(f"   Average flight price: ${df['price_usd'].mean():.2f}")
    print(f"   Median flight price: ${df['price_usd'].median():.2f}")
    
    # Airline insights
    print("\n✈️  AIRLINE INSIGHTS:")
    cheapest_airline = df.groupby('airline')['price_usd'].mean().idxmin()
    most_expensive_airline = df.groupby('airline')['price_usd'].mean().idxmax()
    print(f"   Most affordable airline: {cheapest_airline}")
    print(f"   Most expensive airline: {most_expensive_airline}")
    print(f"   Most flights offered by: {df['airline'].value_counts().idxmax()}")
    
    # Class insights
    print("\n🎫 CLASS INSIGHTS:")
    for class_type in df['class'].unique():
        avg_price = df[df['class'] == class_type]['price_usd'].mean()
        print(f"   {class_type}: ${avg_price:.2f} average")
    
    # Stops insights
    print("\n🛬 STOPS INSIGHTS:")
    for stop in sorted(df['stops'].unique()):
        avg_price = df[df['stops'] == stop]['price_usd'].mean()
        count = len(df[df['stops'] == stop])
        print(f"   {stop} stops: ${avg_price:.2f} average ({count:,} flights)")
    
    # Route insights
    print("\n🗺️  ROUTE INSIGHTS:")
    df['route'] = df['source_city'] + ' → ' + df['destination_city']
    most_common_route = df['route'].value_counts().idxmax()
    most_expensive_route = df.groupby('route')['price_usd'].mean().idxmax()
    cheapest_route = df.groupby('route')['price_usd'].mean().idxmin()
    print(f"   Most common route: {most_common_route}")
    print(f"   Most expensive route: {most_expensive_route}")
    print(f"   Cheapest route: {cheapest_route}")
    
    # Conversion info
    print("\n💱 CONVERSION INFO:")
    print(f"   Exchange rate used: 1 INR = ${df['exchange_rate_used'].iloc[0]:.4f} USD")
    print(f"   Conversion date: {df['conversion_date'].iloc[0]}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Main execution function"""
    print("="*70)
    print("ETL RESULTS VISUALIZATION")
    print("="*70)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Print insights
    print_insights(df)
    
    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(df)
    
    print("\n✓ Analysis complete!")


if __name__ == "__main__":
    main()


