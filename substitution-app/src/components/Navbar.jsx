import React from "react";
import '../styles/Navbar.css';

const Navbar = () => {
    return (
        <nav className='navbar'>
            <h1 className="title">Substitution Scheduler</h1>
            <a href="https://github.com/lailaz5/substitution-scheduler" target="_blank" rel="noopener noreferrer" className="github-button">
                <span>GitHub Project</span>
            </a>
        </nav>
    );
}

export default Navbar;