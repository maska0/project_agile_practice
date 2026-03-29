import React, { useState } from 'react';
import Register from './components/Register';
import CreateEvent from './components/CreateEvent';
import EventList from './components/EventList';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState(null);
  const [activeTab, setActiveTab] = useState('events'); 

  const handleLogin = () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      setIsLoggedIn(true);
      setUserId(user.userId);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    setIsLoggedIn(false);
    setUserId(null);
  };

  if (!isLoggedIn) {
    return <Register onLogin={handleLogin} />;
  }

  return (
    <div>
      <header style={styles.header}>
        <h1 style={styles.logo}> TAP</h1>
        <div style={styles.nav}>
          <button 
            style={{...styles.navButton, ...(activeTab === 'events' ? styles.activeNav : {})}}
            onClick={() => setActiveTab('events')}
          >
             События
          </button>
          <button 
            style={{...styles.navButton, ...(activeTab === 'create' ? styles.activeNav : {})}}
            onClick={() => setActiveTab('create')}
          >
             Создать
          </button>
          <button style={styles.logout} onClick={handleLogout}>
            Выйти
          </button>
        </div>
      </header>
      
      <main>
        {activeTab === 'events' && <EventList />}
        {activeTab === 'create' && <CreateEvent userId={userId} />}
      </main>
    </div>
  );
}

const styles = {
  header: {
    backgroundColor: '#4CAF50',
    color: 'white',
    padding: '15px 30px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
  },
  logo: {
    margin: 0,
    fontSize: '24px'
  },
  nav: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center'
  },
  navButton: {
    padding: '8px 16px',
    backgroundColor: 'transparent',
    color: 'white',
    border: '1px solid white',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'all 0.2s'
  },
  activeNav: {
    backgroundColor: 'white',
    color: '#4CAF50',
    border: '1px solid white'
  },
  logout: {
    padding: '8px 16px',
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '14px',
    marginLeft: '10px'
  }
};

export default App;