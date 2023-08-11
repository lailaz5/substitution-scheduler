import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import TryItOut from './pages/TryItOut'
import './styles/App.css';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/TryItOut" element={<TryItOut />} />
      </Routes>
    </Router>
  );
}

export default App;