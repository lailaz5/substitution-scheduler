import React, { useState, useRef } from 'react';
import Timetable from '../components/Timetable';
import Dropdown from '../components/Dropdown';
import Menu from '../components/Menu';
import '../styles/TryItOut.css';
import axios from 'axios';

const TryItOut = () => {
  const [selectedTeacher, setSelectedTeacher] = useState('');
  const [menuVisible, setMenuVisible] = useState(false);
  const [menuData, setMenuData] = useState({});
  const [loadingMenu, setLoadingMenu] = useState(false);
  const abortControllerRef = useRef(null);

  const handleSelectTeacher = (teacherName) => {
    setSelectedTeacher(teacherName);
    setMenuVisible(false);
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  const handleCellClick = async (day, time) => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    abortControllerRef.current = new AbortController();
    setLoadingMenu(true);

    try {
      const absentTeacher = selectedTeacher;
      const encodedTeacherName = encodeURIComponent(absentTeacher);
      const timetableResponse = await axios.get(`http://localhost:5000/${encodedTeacherName}`, {
        signal: abortControllerRef.current.signal,
      });
      const timetableData = timetableResponse.data;

      const cellData = timetableData[day]?.[time];

      if (!cellData) {
        console.error('No timetable entry found for the selected day and time');
        return;
      }

      if (cellData.attivita) {
        console.log('No substitution needed, teacher has "attivita" scheduled.');
        setMenuVisible(false);
        return;
      }

      const requestData = {
        absent_teacher: absentTeacher,
        day: day,
        timeslot: time,
        classe: cellData.classe,
        materia: cellData.materia,
        insegnanti: cellData.insegnanti,
        aula: cellData.aula,
      };

      console.log('Request Data:', requestData);

      const response = await axios.post('http://localhost:5000/analyze', requestData, {
        signal: abortControllerRef.current.signal,
      });
      const substitutes = response.data;

      setMenuData(substitutes);
      setMenuVisible(true);
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log('Previous request canceled:', error.message);
      } else {
        console.error('Error analyzing timetable cell:', error);
      }
    } finally {
      if (abortControllerRef.current.signal.aborted === false) {
        setLoadingMenu(false);
      }
    }
  };

  return (
    <div className="container">
      <div className="sidebar">
        <div className="dropdown-container">
          <Dropdown onSelectTeacher={handleSelectTeacher} />
        </div>
        {menuVisible && <Menu substitutes={menuData} loading={loadingMenu} />}
      </div>
      <div className="timetable-container">
        {selectedTeacher ? (
          <Timetable teacherName={selectedTeacher} onCellClick={handleCellClick} />
        ) : (
          <p>Seleziona un docente per visualizzarne l'orario.</p>
        )}
      </div>
    </div>
  );
};

export default TryItOut;