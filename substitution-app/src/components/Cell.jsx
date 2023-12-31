import React from 'react';
import '../styles/Cell.css'

const Cell = ({ data }) => {
  if (!data) {
    return <td></td>;
  }

  return (
    <td className="data-cell">
      <div className="data">
        {data.attivita && <p>{data.attivita}</p>}
        <p>{data.classe}</p>
        <p>{data.materia}</p>
        {Array.isArray(data.insegnanti) ? (
          <div>
            {data.insegnanti.map((teacher, index) => (
              <p key={index}>{teacher}</p>
            ))}
          </div>
        ) : (
          <p>{data.insegnanti}</p>
        )}
        <p>{data.aula}</p>
      </div>
    </td>
  );
};

export default Cell;