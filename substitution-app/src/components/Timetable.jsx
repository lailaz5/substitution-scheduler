import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Timetable.css';

const Timetable = ({ teacherName }) => {
  const [timetableData, setTimetableData] = useState([]);
  const [isLoading, setIsLoading] = useState(true); 

  useEffect(() => {
    if (teacherName) {
      const encodedTeacherName = encodeURIComponent(teacherName);
      const url = `http://localhost:5000/${encodedTeacherName}`;
      axios.get(url)
        .then(response => {
          setTimetableData(response.data);
          setIsLoading(false); 
        })
        .catch(error => {
          console.error('Error fetching timetable data:', error);
          setIsLoading(false); 
        });
    }
  }, [teacherName]);

  return (
    <div className="timetable">
      {isLoading ? (
        <div className="loading">Loading...</div>
      ) : (
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
                    {timetableData[day][time]?.attivita && (
                      <p>{timetableData[day][time].attivita}</p>
                    )}
                    <p>{timetableData[day][time]?.classe}</p>
                    <p>{timetableData[day][time]?.materia}</p>
                    {Array.isArray(timetableData[day][time]?.insegnanti) ? (
                      <div>
                        {timetableData[day][time].insegnanti.map((teacher, index) => (
                          <p key={index}>{teacher}</p>
                        ))}
                      </div>
                    ) : (
                      <p>{timetableData[day][time]?.insegnanti}</p>
                    )}
                    <p>{timetableData[day][time]?.aula}</p>
                  </div>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      )}
    </div>
  );
};

export default Timetable;