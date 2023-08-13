import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/Dropdown.css';

const Dropdown = ({ onSelectTeacher }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState('Insegnante da sostituire');
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
    setInputValue('');
    setFilteredOptions(teachersList);
  };

  const handleOptionClick = (option) => {
    setSelectedOption(option);
    setIsOpen(false);
    setInputValue('');
    setFilteredOptions(teachersList);

    // Pass the selected teacher name to the parent component
    onSelectTeacher(option);
  };

  const handleInputChange = (e) => {
    const inputText = e.target.value;
    setInputValue(inputText);
    setFilteredOptions(teachersList.filter(option =>
      option.toLowerCase().includes(inputText.toLowerCase())
    ));
  };

  return (
    <div className="dropdown">
      <div className="header" onClick={toggleDropdown}>
        {selectedOption}
      </div>
      {isOpen && (
        <div className="content">
          <input type="text" value={inputValue} onChange={handleInputChange} placeholder="Cerca un insegnante..."/>
          <ul className="list">
            {filteredOptions.map((option, index) => (
              <li key={index} onClick={() => handleOptionClick(option)}>
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