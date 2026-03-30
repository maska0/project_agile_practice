import mysql.connector
from mysql.connector import Error

class Database:
    
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',       
            'password': 'Asetov01',    
            'database': 'tap_project',
            'charset': 'utf8mb4'
        }
        self.init_tables()
    
    def get_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            return conn
        except Error as e:
            print(f"Ошибка подключения: {e}")
            return None
    

    
    def create_user(self, phone):
        conn = self.get_connection()
        if not conn:
            return {"success": False, "message": "Ошибка БД"}
        
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
            existing = cursor.fetchone()
            
            if existing:
                return {
                    "id": f"user_{existing[0]}",
                    "phone": phone,
                    "success": True
                }
            
            cursor.execute(
                "INSERT INTO users (phone) VALUES (%s)",
                (phone,)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            return {
                "id": f"user_{user_id}",
                "phone": phone,
                "success": True
            }
        except Error as e:
            print(f"Ошибка: {e}")
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_phone(self, phone):
        conn = self.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, phone, name, registered_at FROM users WHERE phone = %s",
            (phone,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return {
                "id": f"user_{row['id']}",
                "phone": row['phone'],
                "name": row['name'],
                "registered_at": row['registered_at']
            }
        return None
    

    
    def save_verification_code(self, phone, code, expires_at):
        conn = self.get_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM verification_codes WHERE phone = %s", (phone,))
            cursor.execute(
                "INSERT INTO verification_codes (phone, code, expires_at) VALUES (%s, %s, %s)",
                (phone, code, expires_at)
            )
            conn.commit()
            return True
        except Error as e:
            print(f"Ошибка: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def get_verification_code(self, phone):
        conn = self.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT code, expires_at FROM verification_codes WHERE phone = %s ORDER BY created_at DESC LIMIT 1",
            (phone,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row:
            return {
                "code": row['code'],
                "expires_at": row['expires_at']
            }
        return None
    
    def delete_verification_code(self, phone):
        conn = self.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM verification_codes WHERE phone = %s", (phone,))
        conn.commit()
        cursor.close()
        conn.close()
    

    
    def create_event(self, event_data):
        conn = self.get_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        try:
            organizer_id = int(event_data['organizer_id'].replace('user_', ''))
            
            cursor.execute('''
                INSERT INTO events (
                    title, description, location, lat, lng, 
                    date, time, price, category, organizer_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                event_data['title'],
                event_data.get('description', ''),
                event_data.get('location', ''),
                event_data.get('lat', 0),
                event_data.get('lng', 0),
                event_data.get('date', ''),
                event_data.get('time', ''),
                event_data.get('price', 0),
                event_data.get('category', 'Другое'),
                organizer_id
            ))
            
            conn.commit()
            event_id = cursor.lastrowid
            return f"event_{event_id}"
        except Error as e:
            print(f"Ошибка: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_all_events(self):
        conn = self.get_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT 
                e.id, e.title, e.description, e.location, 
                e.lat, e.lng, e.date, e.time, e.price, 
                e.category, e.organizer_id, e.created_at,
                u.phone as organizer_phone,
                (SELECT COUNT(*) FROM participants WHERE event_id = e.id) as participants_count
            FROM events e
            LEFT JOIN users u ON e.organizer_id = u.id
            ORDER BY e.date, e.time
        ''')
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        events = []
        for row in rows:
            events.append({
                "id": f"event_{row['id']}",
                "title": row['title'],
                "description": row['description'],
                "location": row['location'],
                "lat": float(row['lat']) if row['lat'] else 0,
                "lng": float(row['lng']) if row['lng'] else 0,
                "date": row['date'],
                "time": row['time'],
                "price": row['price'],
                "category": row['category'],
                "organizer_id": f"user_{row['organizer_id']}",
                "created_at": row['created_at'],
                "organizer_phone": row['organizer_phone'],
                "participants_count": row['participants_count']
            })
        
        return events
def init_tables(self):
    """Создает все необходимые таблицы, если они не существуют"""
    conn = self.get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                phone VARCHAR(20) UNIQUE NOT NULL,
                name VARCHAR(100),
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица кодов подтверждения
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                phone VARCHAR(20) NOT NULL,
                code VARCHAR(10) NOT NULL,
                expires_at BIGINT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица событий
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                location VARCHAR(255),
                lat DECIMAL(10,8) DEFAULT 0,
                lng DECIMAL(11,8) DEFAULT 0,
                date DATE,
                time TIME,
                price DECIMAL(10,2) DEFAULT 0,
                category VARCHAR(100),
                organizer_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Таблица участников (запись на события)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_id INT NOT NULL,
                user_id INT NOT NULL,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_registration (event_id, user_id),
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        print("✅ Таблицы успешно созданы")
        return True
    except Error as e:
        print(f"❌ Ошибка создания таблиц: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
