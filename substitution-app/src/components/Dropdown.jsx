import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Dropdown.css';

const Dropdown = ({ onSelectTeacher }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [teachersList, setTeachersList] = useState([]);
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [inputValue, setInputValue] = useState('');

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
    }
  };

  const handleOptionClick = (option) => {
    setIsOpen(false);
    setInputValue('');
    setFilteredOptions(teachersList);
    onSelectTeacher(option);
  };

  const handleInputChange = (e) => {
    const inputText = e.target.value.trim().toLowerCase();
    setInputValue(inputText);
    setFilteredOptions(teachersList.filter(option => option.toLowerCase().includes(inputText)));
    setIsOpen(true);
  };

  return (
    <div className="dropdown">
      <input
        className="header"
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onFocus={toggleDropdown}
        placeholder="Cerca un insegnante..."
      />
      {isOpen && (
        <div className="content">
          <ul className="list">
            {filteredOptions.map(option => (
              <li key={option} onClick={() => handleOptionClick(option)}>
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