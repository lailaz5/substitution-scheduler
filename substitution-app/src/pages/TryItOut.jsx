import React, { useState } from 'react';
import Dropdown from '../components/Dropdown';
import Timetable from '../components/Timetable';
import Menu from '../components/Menu';
import '../styles/TryItOut.css';

const TryItOut = () => {
  const [selectedTeacher, setSelectedTeacher] = useState('');
  const [menuVisible, setMenuVisible] = useState(false);

  const handleSelectTeacher = (teacherName) => {
    setSelectedTeacher(teacherName);
  };

  const handleCellClick = () => {
    setMenuVisible((prevVisible) => !prevVisible);
  };

  return (
    <div className="container">
      <div className="sidebar">
        <div className="dropdown-container">
          <Dropdown onSelectTeacher={handleSelectTeacher} />
        </div>
        {menuVisible && <Menu onButtonClick={(option) => console.log(option)} />}
      </div>
      <div className="timetable-container">
        {selectedTeacher ? (
          <Timetable teacherName={selectedTeacher} onCellClick={handleCellClick} />
        ) : (
          <p>Seleziona un docente per visualizzare l'orario.</p>
        )}
      </div>
    </div>
  );
};

export default TryItOut;