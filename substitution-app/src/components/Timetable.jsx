import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Timetable.css';
import Cell from './Cell'; 

const Timetable = ({ teacherName, onCellClick }) => {
  const [timetableData, setTimetableData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedCell, setSelectedCell] = useState({ day: '', time: '' });

  useEffect(() => {
    if (teacherName) {
      const encodedTeacherName = encodeURIComponent(teacherName);
      const url = `http://localhost:5000/${encodedTeacherName}`;
      axios
        .get(url)
        .then((response) => {
          setTimetableData(response.data);
          setIsLoading(false);
        })
        .catch((error) => {
          console.error('Error fetching timetable data:', error);
          setErrorMessage('Error fetching timetable data');
          setIsLoading(false);
        });
    }
  }, [teacherName]);

  const handleCellClick = (day, time, data) => {
    setSelectedCell({ day, time });
    onCellClick(day, time, data);
  };

  return (
    <div className="timetable">
      {isLoading ? (
        <div className="loading">Loading...</div>
      ) : timetableData ? (
        typeof timetableData === 'object' ? (
          <table>
            <thead>
              <tr>
                <th> </th>
                {Object.keys(timetableData).map((day) => (
                  <th key={day}>{day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Object.keys(timetableData[Object.keys(timetableData)[0]] || {}).map((time) => (
                <tr key={time}>
                  <td className="time-column">{time}</td>
                  {Object.keys(timetableData).map((day) => (
                    <Cell
                      key={`${day}-${time}`}
                      day={day}
                      time={time}
                      data={timetableData[day][time]}
                      onCellClick={handleCellClick}
                      selected={selectedCell.day === day && selectedCell.time === time}
                    />
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="banner">{timetableData}</div>
        )
      ) : (
        <div className="error-message">{errorMessage}</div>
      )}
    </div>
  );
};

export default Timetable;