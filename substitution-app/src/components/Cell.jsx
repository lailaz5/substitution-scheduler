import React from 'react';
import '../styles/Cell.css';

const Cell = ({ data, day, time, onCellClick, selected }) => {
  const isEmpty = !data || Object.keys(data).length === 0;

  function handleClick() {
    onCellClick(day, time, data);
  }

  return (
    <td
      className={`data-cell ${isEmpty ? 'empty-cell' : ''} ${selected ? 'selected-cell' : ''}`}
      onClick={handleClick}
      data-day={day}
      data-time={time}
    >
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