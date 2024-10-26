import React from 'react';
import '../styles/Menu.css';

const Menu = ({ substitutes, loading }) => {
  return (
    <div className="menu">
      <h2>Suggerimenti</h2>
      {loading ? (
        <p>Ricerca...</p>
      ) : Object.entries(substitutes).length > 0 ? (
        Object.entries(substitutes)
          .sort(([, pointsA], [, pointsB]) => pointsB - pointsA)
          .map(([teacher, points]) => (
            <button key={teacher}>
              {teacher} ({points} punti)
            </button>
          ))
      ) : (
        <p>Non sono disponibili docenti o non deve essere effettuata una supplenza.</p>
      )}
    </div>
  );
};

export default Menu;