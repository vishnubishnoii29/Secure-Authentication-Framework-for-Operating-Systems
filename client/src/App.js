import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Secure Authentication Framework</h1>
        <p>OS Security Project</p>
      </header>
      <main>
        <div className="auth-container">
          <h2>Login</h2>
          <form>
            <div className="form-group">
              <label>Username:</label>
              <input type="text" placeholder="Enter username" />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input type="password" placeholder="Enter password" />
            </div>
            <button type="submit">Login</button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;
