import logo from './logo.svg';
import './App.css';
import React from "react";
import SearchForm from './Search.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>CS172 Final Project</p>
        <SearchForm/>
      </header>
    </div>
  );
}

export default App;
