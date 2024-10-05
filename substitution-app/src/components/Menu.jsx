import React from 'react';
import '../styles/Menu.css';

const Menu = ({ onButtonClick }) => {
  return (
    <div className="menu">
      <h2>Suggestions</h2>
      <button onClick={() => onButtonClick('option1')}>Option 1</button>
      <button onClick={() => onButtonClick('option2')}>Option 2</button>
      <button onClick={() => onButtonClick('option3')}>Option 3</button>
      <button onClick={() => onButtonClick('option4')}>Option 4</button>
    </div>
  );
};

export default Menu;