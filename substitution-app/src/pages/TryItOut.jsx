import React, { useState } from 'react';
import Dropdown from '../components/Dropdown';
import Timetable from '../components/Timetable';
import '../styles/TryItOut.css';

const TryItOut = () => {
  const [selectedTeacher, setSelectedTeacher] = useState('');

  const handleSelectTeacher = (teacherName) => {
    setSelectedTeacher(teacherName);
  };

  return (
    <div className="container">
      <div className="dropdown-container">
        <Dropdown onSelectTeacher={handleSelectTeacher} />
      </div>
      <div className="timetable-container">
        <Timetable teacherName={selectedTeacher} />
      </div>
    </div>
  );
};

export default TryItOut;