"""
Data Loader Module
- Fetch stock prices using yfinance
- Calculate financial metrics
- Load bond and CDS data
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bond_cds_config import (
    BONDS, CDS_PORTFOLIO, MARKET_DATA, 
    get_bond_dataframe, get_cds_dataframe
)

class DataLoader:
    """Load and process market data for bond and CDS portfolio"""
    
    def __init__(self):
        self.valuation_date = pd.to_datetime(MARKET_DATA['valuation_date'])
        self.bond_df = get_bond_dataframe()
        self.cds_df = get_cds_dataframe()
        self.stock_data = {}
        self.financial_metrics = {}
        
    def fetch_stock_data(self, period='2y'):
        """
        Fetch historical stock prices for all companies
        
        Parameters:
        - period: Historical data period (default: 2 years)
        
        Returns:
        - Dictionary of ticker: price DataFrame
        """
        tickers = self.bond_df['ticker'].unique()
        
        print(f"📊 Fetching stock data for {len(tickers)} companies...")
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                
                if hist.empty:
                    print(f"⚠️  {ticker}: No data available")
                    continue
                    
                # Store historical prices
                self.stock_data[ticker] = hist
                
                # Calculate returns
                hist['returns'] = hist['Close'].pct_change()
                
                print(f"✅ {ticker}: {len(hist)} data points loaded")
                
            except Exception as e:
                print(f"❌ {ticker}: Error - {str(e)}")
                
        print(f"\n✅ Successfully loaded data for {len(self.stock_data)} tickers\n")
        return self.stock_data
    
    def calculate_financial_metrics(self):
        """
        Calculate key financial metrics for credit risk analysis
        
        Metrics:
        - Stock volatility (annualized)
        - Current stock price
        - Market cap estimate
        - Distance to default proxy
        """
        print("📈 Calculating financial metrics...")
        
        for ticker in self.stock_data.keys():
            try:
                hist = self.stock_data[ticker]
                
                # Current price
                current_price = hist['Close'].iloc[-1]
                
                # Daily returns volatility (annualized)
                daily_vol = hist['returns'].std()
                annual_vol = daily_vol * np.sqrt(252)  # 252 trading days
                
                # Price statistics
                price_52w_high = hist['Close'].rolling(252).max().iloc[-1]
                price_52w_low = hist['Close'].rolling(252).min().iloc[-1]
                
                # Get company info
                stock = yf.Ticker(ticker)
                info = stock.info
                
                market_cap = info.get('marketCap', np.nan)
                
                self.financial_metrics[ticker] = {
                    'current_price': current_price,
                    'annual_volatility': annual_vol,
                    'market_cap': market_cap,
                    '52w_high': price_52w_high,
                    '52w_low': price_52w_low,
                    'price_change_1m': hist['Close'].pct_change(21).iloc[-1],  # 1 month
                    'price_change_3m': hist['Close'].pct_change(63).iloc[-1],  # 3 months
                    'price_change_1y': hist['Close'].pct_change(252).iloc[-1], # 1 year
                }
                
                print(f"✅ {ticker}: Vol={annual_vol:.2%}, Price=${current_price:.2f}")
                
            except Exception as e:
                print(f"❌ {ticker}: Metrics calculation failed - {str(e)}")
        
        print(f"\n✅ Calculated metrics for {len(self.financial_metrics)} companies\n")
        return self.financial_metrics
    
    def get_correlation_matrix(self):
        """Calculate correlation matrix of stock returns"""
        returns_df = pd.DataFrame()
        
        for ticker, hist in self.stock_data.items():
            returns_df[ticker] = hist['returns']
        
        corr_matrix = returns_df.corr()
        return corr_matrix
    
    def calculate_portfolio_metrics(self):
        """Calculate portfolio-level metrics"""
        bond_df = self.bond_df.copy()
        
        # Add time to maturity
        bond_df['years_to_maturity'] = (
            (bond_df['maturity'] - self.valuation_date).dt.days / 365.25
        )
        
        # Weighted average metrics
        total_value = bond_df['position_size'].sum()
        
        metrics = {
            'total_bond_value': total_value,
            'total_cds_notional': self.cds_df['notional'].sum(),
            'weighted_avg_coupon': (
                (bond_df['coupon'] * bond_df['position_size']).sum() / total_value
            ),
            'weighted_avg_maturity': (
                (bond_df['years_to_maturity'] * bond_df['position_size']).sum() / total_value
            ),
            'weighted_avg_rating': (
                (bond_df['rating_numeric'] * bond_df['position_size']).sum() / total_value
            ),
            'num_bonds': len(bond_df),
            'num_cds': len(self.cds_df),
        }
        
        return metrics
    
    def get_enriched_bond_data(self):
        """Get bond dataframe enriched with stock metrics"""
        enriched = self.bond_df.copy()
        
        # Add financial metrics
        for ticker in enriched['ticker']:
            if ticker in self.financial_metrics:
                metrics = self.financial_metrics[ticker]
                enriched.loc[enriched['ticker'] == ticker, 'stock_price'] = metrics['current_price']
                enriched.loc[enriched['ticker'] == ticker, 'volatility'] = metrics['annual_volatility']
                enriched.loc[enriched['ticker'] == ticker, 'market_cap'] = metrics['market_cap']
        
        # Calculate time to maturity
        enriched['years_to_maturity'] = (
            (enriched['maturity'] - self.valuation_date).dt.days / 365.25
        )
        
        # Calculate bond market value
        enriched['market_value'] = enriched['position_size'] * enriched['current_price'] / 100
        
        return enriched
    
    def get_enriched_cds_data(self):
        """Get CDS dataframe enriched with stock metrics"""
        enriched = self.cds_df.copy()
        
        # Add financial metrics
        for ticker in enriched['ticker']:
            if ticker in self.financial_metrics:
                metrics = self.financial_metrics[ticker]
                enriched.loc[enriched['ticker'] == ticker, 'stock_price'] = metrics['current_price']
                enriched.loc[enriched['ticker'] == ticker, 'volatility'] = metrics['annual_volatility']
        
        return enriched
    
    def export_to_csv(self, output_dir='/home/claude/data'):
        """Export all data to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Bond data
        bond_data = self.get_enriched_bond_data()
        bond_data.to_csv(f'{output_dir}/bond_portfolio.csv', index=False)
        
        # CDS data
        cds_data = self.get_enriched_cds_data()
        cds_data.to_csv(f'{output_dir}/cds_portfolio.csv', index=False)
        
        # Correlation matrix
        corr = self.get_correlation_matrix()
        corr.to_csv(f'{output_dir}/correlation_matrix.csv')
        
        # Financial metrics
        metrics_df = pd.DataFrame.from_dict(self.financial_metrics, orient='index')
        metrics_df.to_csv(f'{output_dir}/financial_metrics.csv')
        
        print(f"\n✅ All data exported to {output_dir}/")
        print(f"   - bond_portfolio.csv")
        print(f"   - cds_portfolio.csv")
        print(f"   - correlation_matrix.csv")
        print(f"   - financial_metrics.csv")
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "=" * 80)
        print("📊 PORTFOLIO DATA SUMMARY REPORT")
        print("=" * 80)
        
        # Portfolio metrics
        port_metrics = self.calculate_portfolio_metrics()
        print(f"\n🎯 Portfolio Overview:")
        print(f"   Total Bond Value:      ${port_metrics['total_bond_value']:,.0f}")
        print(f"   Total CDS Notional:    ${port_metrics['total_cds_notional']:,.0f}")
        print(f"   Number of Bonds:       {port_metrics['num_bonds']}")
        print(f"   Number of CDS:         {port_metrics['num_cds']}")
        print(f"   Avg Coupon:            {port_metrics['weighted_avg_coupon']:.2f}%")
        print(f"   Avg Maturity:          {port_metrics['weighted_avg_maturity']:.2f} years")
        
        # Stock data summary
        print(f"\n📈 Stock Data:")
        print(f"   Companies with data:   {len(self.stock_data)}")
        if self.stock_data:
            avg_vol = np.mean([m['annual_volatility'] for m in self.financial_metrics.values()])
            print(f"   Average Volatility:    {avg_vol:.2%}")
        
        # Highest risk names
        print(f"\n⚠️  Highest Risk Bonds (by CDS spread):")
        cds_sorted = self.cds_df.sort_values('spread_bps', ascending=False)
        for _, row in cds_sorted.head(3).iterrows():
            print(f"   {row['ticker']:6s} - {row['spread_bps']:4.0f} bps ({row['company']})")
        
        print("=" * 80 + "\n")


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    # Initialize data loader
    loader = DataLoader()
    
    # Fetch stock data
    loader.fetch_stock_data(period='2y')
    
    # Calculate financial metrics
    loader.calculate_financial_metrics()
    
    # Calculate correlation
    print("\n📊 Calculating correlation matrix...")
    corr = loader.get_correlation_matrix()
    print(f"✅ Correlation matrix: {corr.shape[0]}x{corr.shape[1]}")
    
    # Export data
    loader.export_to_csv()
    
    # Generate summary
    loader.generate_summary_report()
    
    print("✅ Data loading complete! Ready for risk analysis.\n")
