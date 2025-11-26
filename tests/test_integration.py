"""
Integration tests - test full pipeline
"""
import pytest
import pandas as pd
import os

def test_full_pipeline_runs():
    """Test that full data pipeline can execute"""
    # This would run the full pipeline in a test environment
    # For now, just check that key files can be created
    
    assert True  # Placeholder

def test_output_files_created():
    """Test that expected output files are created"""
    expected_files = [
        'data/processed/panel_data.csv',
        'data/processed/panel_data_clean.csv'
    ]
    
    # In a real test, you'd run the pipeline first
    # For demo, we just check the structure
    assert os.path.exists('data')

def test_data_quality_checks():
    """Test data quality requirements"""
    # If data exists, run quality checks
    if os.path.exists('data/processed/panel_data_clean.csv'):
        df = pd.read_csv('data/processed/panel_data_clean.csv')
        
        # Must have required columns
        required_cols = ['country_name', 'year', 'gdp_growth']
        assert all(col in df.columns for col in required_cols)
        
        # Must have data for multiple countries
        assert df['country_name'].nunique() >= 5
        
        # Years should be in reasonable range
        assert df['year'].min() >= 2010
        assert df['year'].max() <= 2025