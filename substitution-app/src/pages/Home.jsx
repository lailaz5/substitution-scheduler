import React from 'react';
import '../styles/Home.css';

const Home = () => {
  return (
    <div className="banner">
      <img src="/smallLogo.png" alt="Website Logo" className="logo" />
      <div className="button-container">
        <a href="/TryItOut" className="try-button">
          <span>Try it out</span>
        </a>
        <a href="https://github.com/lailaz5/substitution-scheduler" target="_blank" rel="noopener noreferrer" className="github-button">
          <span>GitHub Project</span>
        </a>
      </div>
    </div>
  );
};

export default Home;