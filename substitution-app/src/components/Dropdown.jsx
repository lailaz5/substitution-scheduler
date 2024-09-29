import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Dropdown.css';

const Dropdown = ({ onSelectTeacher }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [teachersList, setTeachersList] = useState([]);
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [selectedTeacher, setSelectedTeacher] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/teachers')
      .then(response => {
        setTeachersList(response.data);
        setFilteredOptions(response.data);
      })
      .catch(error => console.error('Error fetching teachers list:', error));
  }, []);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setInputValue('');
      setFilteredOptions(teachersList);
      setSelectedTeacher(null);
    }
  };

  const handleOptionClick = (option) => {
    setIsOpen(false);
    setInputValue('');
    setFilteredOptions(teachersList);
    setSelectedTeacher(option);
    onSelectTeacher(option);
  };

  const handleInputChange = (e) => {
    const inputText = e.target.value.trim().toLowerCase();
    setInputValue(inputText);
    setFilteredOptions(teachersList.filter(option => option.toLowerCase().includes(inputText)));
    setIsOpen(true);
    setSelectedTeacher(null);
  };

  const getWidthBasedOnContent = () => {
    if (selectedTeacher) {
      return `${selectedTeacher.length + 1}ch`;
    } else if (inputValue) {
      return `${inputValue.length + 1}ch`; 
    } else {
      return '20ch'; 
    }
  };

  return (
    <div className="dropdown">
      <input
        className="header"
        type="text"
        value={selectedTeacher || inputValue}
        onChange={handleInputChange}
        onFocus={toggleDropdown}
        placeholder="Cerca un docente..."
        style={{ width: getWidthBasedOnContent() }} 
      />
      {isOpen && (
        <div className="content">
          <ul className="list">
            {filteredOptions.map(option => (
              <li 
                key={option} 
                onClick={() => handleOptionClick(option)}
                className={selectedTeacher === option ? 'selected' : ''}
              >
                {option}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dropdown;