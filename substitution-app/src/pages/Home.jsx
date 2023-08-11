import React from 'react';
import '../styles/Home.css';

const Home = () => {
  return (
    <div className="banner">
      <h1 className="title">Substitution Scheduler</h1>
      <p className="motto">~ Efficiently Manage Substitutions with Ease ~</p>
      <div className="button-container">
        <a href="/TryItOut" className="try-button">
          <span>Try it out</span>
        </a>
        <a href="https://github.com/lailaz5/substitution-scheduler" className="github-button">
          <span>GitHub Project</span>
        </a>
      </div>
    </div>
  );
};

export default Home;