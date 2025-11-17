"""
Stock database setup script to create SQLite database with mock stock data.
Creates a comprehensive stock market database with companies, prices, and trading data.
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Stock sectors
SECTORS = [
    "Technology", "Healthcare", "Financial Services", "Consumer Cyclical",
    "Communication Services", "Industrials", "Consumer Defensive", "Energy",
    "Utilities", "Real Estate", "Basic Materials", "Consumer Staples"
]

# Sample company names by sector
COMPANIES_BY_SECTOR = {
    "Technology": [
        ("AAPL", "Apple Inc."), ("MSFT", "Microsoft Corporation"), ("GOOGL", "Alphabet Inc."),
        ("AMZN", "Amazon.com Inc."), ("META", "Meta Platforms Inc."), ("NVDA", "NVIDIA Corporation"),
        ("TSLA", "Tesla Inc."), ("ORCL", "Oracle Corporation"), ("CRM", "Salesforce Inc."),
        ("INTC", "Intel Corporation"), ("AMD", "Advanced Micro Devices"), ("ADBE", "Adobe Inc."),
        ("NFLX", "Netflix Inc."), ("PYPL", "PayPal Holdings Inc."), ("UBER", "Uber Technologies Inc.")
    ],
    "Healthcare": [
        ("JNJ", "Johnson & Johnson"), ("UNH", "UnitedHealth Group"), ("PFE", "Pfizer Inc."),
        ("ABBV", "AbbVie Inc."), ("TMO", "Thermo Fisher Scientific"), ("ABT", "Abbott Laboratories"),
        ("DHR", "Danaher Corporation"), ("BMY", "Bristol-Myers Squibb"), ("AMGN", "Amgen Inc."),
        ("GILD", "Gilead Sciences Inc."), ("CVS", "CVS Health Corporation"), ("CI", "Cigna Corporation")
    ],
    "Financial Services": [
        ("JPM", "JPMorgan Chase & Co."), ("BAC", "Bank of America Corp."), ("WFC", "Wells Fargo & Company"),
        ("GS", "Goldman Sachs Group Inc."), ("MS", "Morgan Stanley"), ("C", "Citigroup Inc."),
        ("BLK", "BlackRock Inc."), ("SCHW", "Charles Schwab Corporation"), ("AXP", "American Express Company"),
        ("V", "Visa Inc."), ("MA", "Mastercard Inc."), ("PYPL", "PayPal Holdings Inc.")
    ],
    "Consumer Cyclical": [
        ("TSLA", "Tesla Inc."), ("AMZN", "Amazon.com Inc."), ("HD", "The Home Depot Inc."),
        ("NKE", "Nike Inc."), ("SBUX", "Starbucks Corporation"), ("MCD", "McDonald's Corporation"),
        ("LOW", "Lowe's Companies Inc."), ("TJX", "TJX Companies Inc."), ("BKNG", "Booking Holdings Inc."),
        ("GM", "General Motors Company"), ("F", "Ford Motor Company"), ("TGT", "Target Corporation")
    ],
    "Communication Services": [
        ("GOOGL", "Alphabet Inc."), ("META", "Meta Platforms Inc."), ("NFLX", "Netflix Inc."),
        ("DIS", "The Walt Disney Company"), ("CMCSA", "Comcast Corporation"), ("VZ", "Verizon Communications Inc."),
        ("T", "AT&T Inc."), ("TMUS", "T-Mobile US Inc."), ("EA", "Electronic Arts Inc."),
        ("TTWO", "Take-Two Interactive Software"), ("SPOT", "Spotify Technology"), ("SNAP", "Snap Inc.")
    ],
    "Energy": [
        ("XOM", "Exxon Mobil Corporation"), ("CVX", "Chevron Corporation"), ("COP", "ConocoPhillips"),
        ("SLB", "Schlumberger Limited"), ("EOG", "EOG Resources Inc."), ("MPC", "Marathon Petroleum Corporation"),
        ("VLO", "Valero Energy Corporation"), ("PSX", "Phillips 66"), ("HAL", "Halliburton Company"),
        ("OXY", "Occidental Petroleum Corporation")
    ],
    "Industrials": [
        ("BA", "The Boeing Company"), ("CAT", "Caterpillar Inc."), ("GE", "General Electric Company"),
        ("HON", "Honeywell International Inc."), ("UPS", "United Parcel Service Inc."), ("RTX", "Raytheon Technologies"),
        ("DE", "Deere & Company"), ("LMT", "Lockheed Martin Corporation"), ("EMR", "Emerson Electric Co."),
        ("ETN", "Eaton Corporation")
    ],
    "Consumer Defensive": [
        ("WMT", "Walmart Inc."), ("PG", "Procter & Gamble Company"), ("KO", "The Coca-Cola Company"),
        ("PEP", "PepsiCo Inc."), ("COST", "Costco Wholesale Corporation"), ("CL", "Colgate-Palmolive Company"),
        ("KMB", "Kimberly-Clark Corporation"), ("GIS", "General Mills Inc."), ("CPB", "Campbell Soup Company"),
        ("SJM", "The J.M. Smucker Company")
    ],
    "Utilities": [
        ("NEE", "NextEra Energy Inc."), ("DUK", "Duke Energy Corporation"), ("SO", "The Southern Company"),
        ("AEP", "American Electric Power"), ("EXC", "Exelon Corporation"), ("XEL", "Xcel Energy Inc."),
        ("SRE", "Sempra Energy"), ("WEC", "WEC Energy Group Inc."), ("ES", "Eversource Energy"),
        ("PEG", "Public Service Enterprise Group")
    ],
    "Real Estate": [
        ("AMT", "American Tower Corporation"), ("PLD", "Prologis Inc."), ("EQIX", "Equinix Inc."),
        ("PSA", "Public Storage"), ("WELL", "Welltower Inc."), ("SPG", "Simon Property Group Inc."),
        ("O", "Realty Income Corporation"), ("AVB", "AvalonBay Communities Inc."), ("EQR", "Equity Residential"),
        ("VTR", "Ventas Inc.")
    ],
    "Basic Materials": [
        ("LIN", "Linde plc"), ("APD", "Air Products and Chemicals Inc."), ("ECL", "Ecolab Inc."),
        ("SHW", "The Sherwin-Williams Company"), ("DD", "DuPont de Nemours Inc."), ("PPG", "PPG Industries Inc."),
        ("NEM", "Newmont Corporation"), ("FCX", "Freeport-McMoRan Inc."), ("VALE", "Vale S.A."),
        ("NUE", "Nucor Corporation")
    ]
}

def generate_stock_data():
    """Generate comprehensive stock data."""
    stocks = []
    stock_id = 1
    
    # Generate stocks from all sectors
    for sector, companies in COMPANIES_BY_SECTOR.items():
        for ticker, company_name in companies:
            # Base price varies by sector and company
            base_price = random.uniform(20, 500)
            
            # Market cap calculation (price * shares outstanding)
            shares_outstanding = random.randint(100000000, 10000000000)  # 100M to 10B shares
            market_cap = base_price * shares_outstanding
            
            # Generate multiple price points over time (last 90 days)
            base_date = datetime.now() - timedelta(days=90)
            
            for day_offset in range(0, 90, 1):  # Daily data for 90 days
                date = base_date + timedelta(days=day_offset)
                
                # Price variation (random walk)
                price_change = random.uniform(-0.05, 0.05)  # ±5% daily change
                current_price = base_price * (1 + price_change)
                base_price = current_price  # Update for next day
                
                # Volume (higher on volatile days)
                volatility = abs(price_change)
                base_volume = random.randint(1000000, 50000000)
                volume = int(base_volume * (1 + volatility * 2))
                
                # Calculate change and change percent
                prev_price = current_price / (1 + price_change) if price_change != 0 else current_price
                change = current_price - prev_price
                change_percent = (change / prev_price * 100) if prev_price > 0 else 0
                
                stocks.append((
                    stock_id,
                    ticker,
                    company_name,
                    sector,
                    round(current_price, 2),
                    round(change, 2),
                    round(change_percent, 2),
                    volume,
                    round(market_cap, 2),
                    date.strftime('%Y-%m-%d')
                ))
            
            stock_id += 1
    
    return stocks

def create_database():
    """Create database and tables."""
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()
    
    # Create stocks table with comprehensive fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            ticker TEXT NOT NULL,
            company_name TEXT NOT NULL,
            sector TEXT,
            price REAL NOT NULL,
            change REAL,
            change_percent REAL,
            volume INTEGER,
            market_cap REAL,
            date DATE,
            UNIQUE(stock_id, date)
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_ticker_date ON stocks(ticker, date)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_sector ON stocks(sector)
    ''')
    
    conn.commit()
    return conn, cursor

def populate_database(cursor, conn):
    """Populate database with stock data."""
    print("Generating stock data...")
    stocks = generate_stock_data()
    
    print(f"Inserting {len(stocks)} stock records...")
    cursor.executemany('''
        INSERT INTO stocks (stock_id, ticker, company_name, sector, price, change, change_percent, volume, market_cap, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', stocks)
    
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(DISTINCT ticker) FROM stocks")
    unique_stocks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM stocks")
    total_records = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(date), MAX(date) FROM stocks")
    date_range = cursor.fetchone()
    
    print(f"\nDatabase created successfully!")
    print(f"- Unique stocks: {unique_stocks}")
    print(f"- Total records: {total_records}")
    print(f"- Date range: {date_range[0]} to {date_range[1]}")
    print(f"- Sectors: {len(SECTORS)}")
    
    # Show sample data
    cursor.execute("""
        SELECT ticker, company_name, sector, price, volume, date
        FROM stocks
        WHERE date = (SELECT MAX(date) FROM stocks)
        LIMIT 10
    """)
    
    print(f"\nSample of latest stock data:")
    print("-" * 100)
    for row in cursor.fetchall():
        print(f"  {row[0]:6s} | {row[1]:30s} | {row[2]:20s} | ${row[3]:8.2f} | {row[4]:>12,} | {row[5]}")

if __name__ == "__main__":
    conn, cursor = create_database()
    populate_database(cursor, conn)
    conn.close()
    print("\nStock database setup complete!")

