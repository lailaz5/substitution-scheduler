import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Timetable.css';

const Timetable = ({ teacherName }) => {
  const [timetableData, setTimetableData] = useState([]);

  useEffect(() => {
    if (teacherName) {
      const encodedTeacherName = encodeURIComponent(teacherName);
      const url = `http://localhost:5000/${encodedTeacherName}`;
      axios.get(url)
        .then(response => {
          setTimetableData(response.data);
        })
        .catch(error => console.error('Error fetching timetable data:', error));
    }
  }, [teacherName]);

  return (
    <div className="timetable">
      <table>
        <thead>
          <tr>
            <th> </th>
            {Object.keys(timetableData).map(day => (
              <th key={day}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Object.keys(timetableData[Object.keys(timetableData)[0]] || {}).map(time => (
            <tr key={time}>
              <td className="time-column">{time}</td>
              {Object.keys(timetableData).map(day => (
                <td key={day} className="data-cell">
                  {timetableData[day][time] && (
                    <div className="data">
                      <p>{timetableData[day][time]?.classe}</p>
                      <p>{timetableData[day][time]?.materia}</p>
                      <p>{timetableData[day][time]?.insegnanti}</p>
                      <p>{timetableData[day][time]?.aula}</p>
                      {timetableData[day][time]?.attivita && (
                        <p>{timetableData[day][time].attivita}</p>
                      )}
                    </div>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Timetable;