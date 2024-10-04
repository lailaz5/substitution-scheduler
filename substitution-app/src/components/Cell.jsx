import React from 'react';
import '../styles/Cell.css';

const Cell = ({ data }) => {
  const isEmpty = !data || Object.keys(data).length === 0;

  function handleClick() {
    alert('LeLeLe!'); // change this function with the suggestion bubble or side menu (use new API endpoint)
  }

  return (
    <td className={`data-cell ${isEmpty ? 'empty-cell' : ''}`} onClick={handleClick}>
      {isEmpty ? (
        <div className="empty-cell-content">&nbsp;</div>
      ) : (
        <div className="data">
          {Object.entries(data).map(([key, value], index) => (
            <div key={index}>
              {Array.isArray(value) ? (
                value.map((item, idx) => <p key={idx}>{item}</p>)
              ) : (
                <p>{value}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </td>
  );
};

export default Cell;