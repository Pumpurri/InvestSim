import React, { useState } from 'react';
import StockPrice from './components/StockPrice';

function App() {
  const [stockSymbol, setStockSymbol] = useState('AAPL');
  const [inputValue, setInputValue] = useState(''); 

  const handleSubmit = (e) => {
    e.preventDefault(); 
    if (inputValue.trim() !== '') {
      setStockSymbol(inputValue.trim().toUpperCase()); 
      setInputValue(''); 
    }
  };

  return (
    <div className="App" style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Stock Paper Trader</h1>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <label htmlFor="stock-symbol">Enter Stock Symbol:</label><br />
        <input
          type="text"
          id="stock-symbol"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="e.g., AAPL"
          style={{ padding: '8px', width: '200px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '8px 16px' }}>Get Price</button>
      </form>

      <StockPrice symbol={stockSymbol} />
    </div>
  );
}

export default App;