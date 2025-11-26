"""
Tests for data cleaning module
"""
import pytest
import pandas as pd
import numpy as np
from src.data_cleaning import handle_missing_values, remove_outliers

@pytest.fixture
def sample_data():
    """Create sample test data"""
    return pd.DataFrame({
        'country_name': ['USA', 'USA', 'USA', 'UK', 'UK', 'UK'],
        'year': [2018, 2019, 2020, 2018, 2019, 2020],
        'gdp_growth': [2.5, 2.2, np.nan, 1.8, np.nan, -9.8],
        'unemployment_rate': [4.0, 3.8, 8.1, 4.5, 4.2, 5.0],
        'cases_per_million': [0, 0, 1000, 0, 0, 1500]
    })

def test_handle_missing_values(sample_data):
    """Test missing value handling"""
    cleaned = handle_missing_values(sample_data)
    
    # Should have fewer missing values
    assert cleaned.isnull().sum().sum() <= sample_data.isnull().sum().sum()
    
    # Should preserve data shape
    assert len(cleaned) == len(sample_data)

def test_remove_outliers():
    """Test outlier removal"""
    df = pd.DataFrame({
        'country_name': ['USA'] * 10,
        'year': range(2014, 2024),
        'gdp_growth': [2.5, 2.6, 2.4, 2.3, 2.5, 2.7, -50, 2.4, 2.5, 2.6]
    })
    
    cleaned = remove_outliers(df, ['gdp_growth'], n_std=3)
    
    # Should remove the extreme outlier (-50)
    assert len(cleaned) < len(df)
    assert cleaned['gdp_growth'].min() > -50

def test_data_types(sample_data):
    """Test that data types are appropriate"""
    assert sample_data['year'].dtype in [np.int64, np.int32]
    assert sample_data['gdp_growth'].dtype in [np.float64, np.float32]