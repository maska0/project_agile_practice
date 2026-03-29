import React, { useState, useEffect } from 'react';
import axios from 'axios';

function EventList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/events');
      setEvents(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка загрузки событий:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={styles.loading}>Загрузка событий...</div>;
  }

  return (
    <div style={styles.container}>
      <h2>Ближайшие события</h2>
      
      {events.length === 0 ? (
        <p style={styles.empty}>Пока нет событий. Создайте первое!</p>
      ) : (
        <div style={styles.grid}>
          {events.map(event => (
            <div key={event.id} style={styles.card}>
              <h3 style={styles.title}>{event.title}</h3>
              
              <div style={styles.info}>
                <p> {event.date} в {event.time}</p>
                <p> {event.location || 'Место не указано'}</p>
                <p> {event.category}</p>
                <p style={event.price === 0 ? styles.free : styles.price}>
                  {event.price === 0 ? '🆓 Бесплатно' : ` ${event.price} тг`}
                </p>
              </div>
              
              <button 
                style={styles.button}
                onClick={() => alert(`Вы записаны на "${event.title}"!`)}
              >
                Записаться
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '20px auto',
    padding: '20px'
  },
  loading: {
    textAlign: 'center',
    fontSize: '18px',
    color: '#666',
    marginTop: '50px'
  },
  empty: {
    textAlign: 'center',
    fontSize: '18px',
    color: '#999',
    marginTop: '50px'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
    marginTop: '20px'
  },
  card: {
    border: '1px solid #ddd',
    borderRadius: '10px',
    padding: '20px',
    backgroundColor: 'white',
    boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    transition: 'transform 0.2s',
    cursor: 'pointer',
    ':hover': {
      transform: 'translateY(-5px)',
      boxShadow: '0 5px 15px rgba(0,0,0,0.2)'
    }
  },
  title: {
    margin: '0 0 10px 0',
    color: '#333',
    fontSize: '20px'
  },
  info: {
    color: '#666',
    fontSize: '14px',
    lineHeight: '1.6'
  },
  free: {
    color: '#4CAF50',
    fontWeight: 'bold',
    fontSize: '16px'
  },
  price: {
    color: '#FF9800',
    fontWeight: 'bold',
    fontSize: '16px'
  },
  button: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    fontSize: '16px',
    cursor: 'pointer',
    marginTop: '15px',
    ':hover': {
      backgroundColor: '#45a049'
    }
  }
};

export default EventList;