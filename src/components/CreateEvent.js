import React, { useState } from 'react';
import axios from 'axios';

function CreateEvent({ userId }) {
  const [form, setForm] = useState({
    title: '',
    description: '',
    location: '',
    date: '',
    time: '',
    price: 0,
    category: 'Творчество'
  });
  
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios.post('http://localhost:5000/api/create-event', {
        ...form,
        organizer_id: userId,
        lat: 43.2385,
        lng: 76.9456
      });
      
      if (response.data.success) {
        setMessage('Событие создано!');
        setForm({
          title: '',
          description: '',
          location: '',
          date: '',
          time: '',
          price: 0,
          category: 'Творчество'
        });
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage('Ошибка сервера');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Создать новое событие</h2>
      
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          name="title"
          placeholder="Название *"
          value={form.title}
          onChange={handleChange}
          style={styles.input}
          required
        />
        
        <textarea
          name="description"
          placeholder="Описание"
          value={form.description}
          onChange={handleChange}
          style={styles.textarea}
          rows="4"
        />
        
        <input
          name="location"
          placeholder="Место проведения"
          value={form.location}
          onChange={handleChange}
          style={styles.input}
        />
        
        <div style={styles.row}>
          <input
            name="date"
            type="date"
            value={form.date}
            onChange={handleChange}
            style={{...styles.input, width: '48%'}}
          />
          <input
            name="time"
            type="time"
            value={form.time}
            onChange={handleChange}
            style={{...styles.input, width: '48%'}}
          />
        </div>
        
        <div style={styles.row}>
          <input
            name="price"
            type="number"
            placeholder="Цена (0 - бесплатно)"
            value={form.price}
            onChange={handleChange}
            style={{...styles.input, width: '48%'}}
          />
          
          <select
            name="category"
            value={form.category}
            onChange={handleChange}
            style={{...styles.input, width: '48%'}}
          >
            <option>Творчество</option>
            <option>Образование</option>
            <option>Спорт</option>
            <option>Волонтерство</option>
            <option>Встречи</option>
          </select>
        </div>
        
        <button type="submit" style={styles.button}>
          Опубликовать событие
        </button>
      </form>
      
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px',
    margin: '20px auto',
    padding: '20px'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px'
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ddd'
  },
  textarea: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ddd',
    fontFamily: 'inherit'
  },
  row: {
    display: 'flex',
    justifyContent: 'space-between'
  },
  button: {
    padding: '15px',
    fontSize: '16px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    marginTop: '10px'
  },
  message: {
    marginTop: '20px',
    color: '#666',
    textAlign: 'center'
  }
};

export default CreateEvent;