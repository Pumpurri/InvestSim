import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

function StockPrice({ symbol }) {
  const [priceData, setPriceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStockPrice = async (symbol) => {
    if (!symbol) return;
  
    setLoading(true);
    setError(null);
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/stocks/stock_gen_info/${symbol}/`, {
        headers: {
          'Accept': 'application/json',
        },
      });
  
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`Stock with symbol '${symbol}' not found.`);
        } else {
          throw new Error(`Failed to fetch stock price: ${response.status} ${response.statusText}`);
        }
      }
  
      const data = await response.json();
      setPriceData(data);
    } catch (err) {
      setError(err.message);
      setPriceData(null);
    } finally {
      setLoading(false);
    }
  };
  

  useEffect(() => {
    fetchStockPrice(symbol);

    const intervalId = setInterval(() => fetchStockPrice(symbol), 30000);

    return () => clearInterval(intervalId);
  }, [symbol]);

  return (
    <div>
      <h2>Current Stock Price for {symbol}</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <div>
          <p style={{ color: 'red' }}>Error fetching stock price: {error}</p>
          <button onClick={() => fetchStockPrice(symbol)}>Retry</button>
        </div>
      ) : priceData ? (
        <div>
          <p><strong>Name:</strong> {priceData.name}</p>
          <p><strong>Current Price:</strong> ${priceData.current_price}</p>
          <p><strong>Last Updated:</strong> {new Date(priceData.last_updated).toLocaleString()}</p>
        </div>
      ) : (
        <p>No data available.</p>
      )}
    </div>
  );
}

StockPrice.propTypes = {
  symbol: PropTypes.string.isRequired,
};

export default StockPrice;