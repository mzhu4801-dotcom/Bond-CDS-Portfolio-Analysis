"""
Corporate Bond + CDS Portfolio Configuration
Portfolio Size: $100M ($70M Bonds + $30M CDS Notional)
"""

import pandas as pd
from datetime import datetime

# ===== BOND PORTFOLIO CONFIGURATION =====
BONDS = {
    # Tech/TMT Sector - $15M
    'TSLA': {
        'company': 'Tesla Inc',
        'sector': 'Tech/TMT',
        'position_size': 5_000_000,
        'coupon': 5.30,  # Annual coupon rate %
        'maturity': '2028-08-15',
        'rating': 'BB+',  # S&P rating
        'rating_numeric': 7,  # BB+ = 7 (higher is better)
        'issue_price': 100,
        'current_price': 98.5,  # Estimated market price
    },
    'NFLX': {
        'company': 'Netflix Inc',
        'sector': 'Tech/TMT',
        'position_size': 5_000_000,
        'coupon': 5.875,
        'maturity': '2029-11-15',
        'rating': 'BB+',
        'rating_numeric': 7,
        'issue_price': 100,
        'current_price': 99.2,
    },
    'T': {
        'company': 'AT&T Inc',
        'sector': 'Tech/TMT',
        'position_size': 5_000_000,
        'coupon': 4.75,
        'maturity': '2030-05-15',
        'rating': 'BBB',
        'rating_numeric': 10,
        'issue_price': 100,
        'current_price': 97.8,
    },
    
    # Energy Sector - $15M
    'XOM': {
        'company': 'Exxon Mobil Corp',
        'sector': 'Energy',
        'position_size': 5_000_000,
        'coupon': 4.23,
        'maturity': '2029-03-19',
        'rating': 'AA-',
        'rating_numeric': 13,
        'issue_price': 100,
        'current_price': 101.2,
    },
    'CVX': {
        'company': 'Chevron Corp',
        'sector': 'Energy',
        'position_size': 5_000_000,
        'coupon': 4.95,
        'maturity': '2028-05-16',
        'rating': 'AA-',
        'rating_numeric': 13,
        'issue_price': 100,
        'current_price': 100.8,
    },
    'OXY': {
        'company': 'Occidental Petroleum',
        'sector': 'Energy',
        'position_size': 5_000_000,
        'coupon': 6.125,
        'maturity': '2027-01-01',
        'rating': 'BBB-',
        'rating_numeric': 9,
        'issue_price': 100,
        'current_price': 99.5,
    },
    
    # Financial Sector - $15M
    'BAC': {
        'company': 'Bank of America Corp',
        'sector': 'Financial',
        'position_size': 5_000_000,
        'coupon': 5.015,
        'maturity': '2029-07-22',
        'rating': 'A-',
        'rating_numeric': 11,
        'issue_price': 100,
        'current_price': 99.8,
    },
    'C': {
        'company': 'Citigroup Inc',
        'sector': 'Financial',
        'position_size': 5_000_000,
        'coupon': 5.316,
        'maturity': '2028-03-26',
        'rating': 'BBB+',
        'rating_numeric': 10,
        'issue_price': 100,
        'current_price': 99.3,
    },
    'GS': {
        'company': 'Goldman Sachs Group',
        'sector': 'Financial',
        'position_size': 5_000_000,
        'coupon': 4.75,
        'maturity': '2030-10-21',
        'rating': 'A-',
        'rating_numeric': 11,
        'issue_price': 100,
        'current_price': 98.9,
    },
    
    # Industrial/Aviation Sector - $15M
    'BA': {
        'company': 'Boeing Co',
        'sector': 'Industrial',
        'position_size': 5_000_000,
        'coupon': 5.705,
        'maturity': '2028-05-01',
        'rating': 'BBB-',
        'rating_numeric': 9,
        'issue_price': 100,
        'current_price': 97.2,
    },
    'F': {
        'company': 'Ford Motor Co',
        'sector': 'Industrial',
        'position_size': 5_000_000,
        'coupon': 7.40,
        'maturity': '2027-11-01',
        'rating': 'BB+',
        'rating_numeric': 7,
        'issue_price': 100,
        'current_price': 98.8,
    },
    'AAL': {
        'company': 'American Airlines',
        'sector': 'Industrial',
        'position_size': 5_000_000,
        'coupon': 8.50,
        'maturity': '2026-05-01',
        'rating': 'B',
        'rating_numeric': 5,
        'issue_price': 100,
        'current_price': 96.5,
    },
    
    # Retail/Consumer Sector - $10M
    'M': {
        'company': "Macy's Inc",
        'sector': 'Retail',
        'position_size': 4_000_000,
        'coupon': 6.70,
        'maturity': '2027-07-15',
        'rating': 'BB-',
        'rating_numeric': 6,
        'issue_price': 100,
        'current_price': 95.8,
    },
    'CCL': {
        'company': 'Carnival Corp',
        'sector': 'Retail',
        'position_size': 3_000_000,
        'coupon': 9.875,
        'maturity': '2028-08-01',
        'rating': 'B-',
        'rating_numeric': 4,
        'issue_price': 100,
        'current_price': 97.3,
    },
    'MGM': {
        'company': 'MGM Resorts',
        'sector': 'Retail',
        'position_size': 3_000_000,
        'coupon': 6.75,
        'maturity': '2027-05-01',
        'rating': 'BB-',
        'rating_numeric': 6,
        'issue_price': 100,
        'current_price': 98.1,
    },
}

# ===== CDS PORTFOLIO CONFIGURATION =====
CDS_PORTFOLIO = {
    'TSLA': {
        'company': 'Tesla Inc',
        'notional': 5_000_000,
        'tenor': 5,  # years
        'spread_bps': 280,  # CDS spread in basis points
        'recovery_rate': 0.40,
        'contract_date': '2025-01-17',
    },
    'NFLX': {
        'company': 'Netflix Inc',
        'notional': 5_000_000,
        'tenor': 5,
        'spread_bps': 220,
        'recovery_rate': 0.40,
        'contract_date': '2025-01-17',
    },
    'AAL': {
        'company': 'American Airlines',
        'notional': 5_000_000,
        'tenor': 5,
        'spread_bps': 450,
        'recovery_rate': 0.35,
        'contract_date': '2025-01-17',
    },
    'F': {
        'company': 'Ford Motor Co',
        'notional': 5_000_000,
        'tenor': 5,
        'spread_bps': 320,
        'recovery_rate': 0.40,
        'contract_date': '2025-01-17',
    },
    'M': {
        'company': "Macy's Inc",
        'notional': 5_000_000,
        'tenor': 5,
        'spread_bps': 380,
        'recovery_rate': 0.35,
        'contract_date': '2025-01-17',
    },
    'OXY': {
        'company': 'Occidental Petroleum',
        'notional': 5_000_000,
        'tenor': 5,
        'spread_bps': 240,
        'recovery_rate': 0.40,
        'contract_date': '2025-01-17',
    },
}

# ===== MARKET DATA CONFIGURATION =====
MARKET_DATA = {
    'risk_free_rate': 0.0425,  # Current US 5Y Treasury yield
    'valuation_date': '2025-01-17',
}

# ===== RATING SCALE =====
RATING_SCALE = {
    'AAA': 15, 'AA+': 14, 'AA': 14, 'AA-': 13,
    'A+': 12, 'A': 12, 'A-': 11,
    'BBB+': 10, 'BBB': 10, 'BBB-': 9,
    'BB+': 7, 'BB': 7, 'BB-': 6,
    'B+': 5, 'B': 5, 'B-': 4,
    'CCC+': 3, 'CCC': 3, 'CCC-': 2,
    'CC': 1, 'C': 1, 'D': 0
}

# Helper function to convert to DataFrame
def get_bond_dataframe():
    """Convert bond portfolio to pandas DataFrame"""
    df = pd.DataFrame.from_dict(BONDS, orient='index')
    df.index.name = 'ticker'
    df.reset_index(inplace=True)
    df['maturity'] = pd.to_datetime(df['maturity'])
    return df

def get_cds_dataframe():
    """Convert CDS portfolio to pandas DataFrame"""
    df = pd.DataFrame.from_dict(CDS_PORTFOLIO, orient='index')
    df.index.name = 'ticker'
    df.reset_index(inplace=True)
    df['contract_date'] = pd.to_datetime(df['contract_date'])
    return df

# Portfolio Summary
def print_portfolio_summary():
    """Print portfolio summary statistics"""
    bond_df = get_bond_dataframe()
    cds_df = get_cds_dataframe()
    
    print("=" * 70)
    print("BOND + CDS PORTFOLIO SUMMARY")
    print("=" * 70)
    print(f"\nBond Portfolio: ${bond_df['position_size'].sum():,.0f}")
    print(f"CDS Notional:   ${cds_df['notional'].sum():,.0f}")
    print(f"Total Exposure: ${bond_df['position_size'].sum() + cds_df['notional'].sum():,.0f}")
    
    print("\n--- By Sector ---")
    print(bond_df.groupby('sector')['position_size'].sum().apply(lambda x: f"${x:,.0f}"))
    
    print("\n--- By Rating ---")
    print(bond_df.groupby('rating')['position_size'].sum().apply(lambda x: f"${x:,.0f}"))
    
    print("\n--- Average Metrics ---")
    print(f"Avg Coupon:     {bond_df['coupon'].mean():.2f}%")
    print(f"Avg CDS Spread: {cds_df['spread_bps'].mean():.0f} bps")
    print(f"Avg Rating:     {bond_df['rating_numeric'].mean():.1f} ({get_rating_from_numeric(bond_df['rating_numeric'].mean())})")
    print("=" * 70)

def get_rating_from_numeric(num):
    """Convert numeric rating back to letter rating"""
    for rating, value in RATING_SCALE.items():
        if abs(value - num) < 0.5:
            return rating
    return "N/A"

if __name__ == "__main__":
    print_portfolio_summary()
