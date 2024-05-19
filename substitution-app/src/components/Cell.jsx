import React from 'react';
import '../styles/Cell.css';

const Cell = ({ data }) => {
  const isEmpty = !data || Object.keys(data).length === 0;

  return (
    <td className={`data-cell ${isEmpty ? 'empty-cell' : ''}`}>
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