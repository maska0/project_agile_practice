

import React, { useState } from 'react';
import axios from 'axios';

function Register({ onLogin }) {
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [step, setStep] = useState(1); 
  const [message, setMessage] = useState('');

  const requestCode = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/request-code', {
        phone: phone
      });
      
      if (response.data.success) {
        setStep(2);
        setMessage('Код отправлен! Проверьте телефон');
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage('Ошибка сервера');
    }
  };

  const verifyCode = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/verify-code', {
        phone: phone,
        code: code
      });
      
      if (response.data.success) {
        setMessage('Успешная регистрация!');
        // Сохраняем пользователя
        localStorage.setItem('user', JSON.stringify({
          phone: phone,
          userId: response.data.user_id
        }));
        onLogin();
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      setMessage('Ошибка сервера');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Регистрация в TAP</h2>
      
      {step === 1 ? (
        <div style={styles.form}>
          <input
            type="tel"
            placeholder="87771234567"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            style={styles.input}
          />
          <button onClick={requestCode} style={styles.button}>
            Получить код
          </button>
        </div>
      ) : (
        <div style={styles.form}>
          <p>Код отправлен на {phone}</p>
          <input
            type="text"
            placeholder="6-значный код"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            style={styles.input}
          />
          <button onClick={verifyCode} style={styles.button}>
            Подтвердить
          </button>
          <button 
            onClick={() => setStep(1)} 
            style={{...styles.button, backgroundColor: '#666'}}
          >
            Назад
          </button>
        </div>
      )}
      
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '400px',
    margin: '50px auto',
    padding: '20px',
    textAlign: 'center'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px'
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ddd'
  },
  button: {
    padding: '10px',
    fontSize: '16px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer'
  },
  message: {
    marginTop: '20px',
    color: '#666'
  }
};

export default Register;