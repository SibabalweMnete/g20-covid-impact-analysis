"""
Tests for data collection module
"""
import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.data_collection import DataCollector

@pytest.fixture
def collector():
    """Create a DataCollector instance for testing"""
    return DataCollector()

def test_collector_initialization(collector):
    """Test that DataCollector initializes correctly"""
    assert len(collector.countries) == 10
    assert collector.start_year == 2015
    assert collector.end_year == 2023

def test_country_codes(collector):
    """Test that country codes are valid ISO codes"""
    valid_codes = ['USA', 'GBR', 'DEU', 'FRA', 'JPN', 
                   'CHN', 'IND', 'BRA', 'ZAF', 'AUS']
    assert all(code in valid_codes for code in collector.countries.keys())

@patch('src.data_collection.requests.get')
def test_world_bank_api_success(mock_get, collector):
    """Test successful World Bank API call"""
    # Mock API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        None,
        [{'date': '2020', 'value': 2.5}]
    ]
    mock_get.return_value = mock_response
    
    # Test
    df = collector.fetch_world_bank_data('NY.GDP.MKTP.KD.ZG', 'gdp_growth')
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'country_name' in df.columns
    assert 'value' in df.columns

@patch('src.data_collection.requests.get')
def test_world_bank_api_failure(mock_get, collector):
    """Test handling of API failures"""
    mock_get.side_effect = Exception("API Error")
    
    # Should not crash, should return empty or partial data
    df = collector.fetch_world_bank_data('NY.GDP.MKTP.KD.ZG', 'gdp_growth')
    
    assert isinstance(df, pd.DataFrame)

def test_stimulus_data_creation(collector):
    """Test manual stimulus data creation"""
    df = collector.create_stimulus_data()
    
    assert len(df) == 10
    assert 'country_name' in df.columns
    assert 'stimulus_pct_gdp_2020' in df.columns
    assert df['stimulus_pct_gdp_2020'].min() > 0

@patch('src.data_collection.pd.read_csv')
def test_covid_data_fetch(mock_read_csv, collector):
    """Test COVID data fetching"""
    # Mock COVID data
    mock_df = pd.DataFrame({
        'location': ['United States', 'United Kingdom'],
        'date': ['2020-01-01', '2020-01-02'],
        'total_cases': [100, 200],
        'total_deaths': [5, 10],
        'total_cases_per_million': [0.5, 0.6],
        'total_deaths_per_million': [0.01, 0.02]
    })
    mock_read_csv.return_value = mock_df
    
    df = collector.fetch_covid_data()
    
    assert isinstance(df, pd.DataFrame)
    assert 'country_name' in df.columns or 'location' in df.columns