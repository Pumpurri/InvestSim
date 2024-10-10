import React, { useState, useEffect } from 'react';

function StockPrice() {
  const [price, setPrice] = useState(null);      
  const [error, setError] = useState(null);      

  useEffect(() => {
    async function fetchStockPrice(symbol) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/stocks/stock_gen_info/${symbol}/`);  
        if (!response.ok) {
          throw new Error('Failed to fetch stock price');
        }
        const data = await response.json();
        setPrice(data.current_price);            
      } catch (err) {
        setError(err.message);
      }
    }

    fetchStockPrice('${symbol}');                     
  }, []);                                        

  return (
    <div>
      <h2>Current Stock Price</h2>
      {error ? (
        <p>Error fetching stock price: {error}</p>
        ) : (
        price ? <p>The stock price is: ${price}</p> : <p>Loading...</p>
      )}
    </div>
  );
}

export default StockPrice;
