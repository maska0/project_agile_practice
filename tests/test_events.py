import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import AuthService
from app.events import EventService
from database import Database

class TestEvents(unittest.TestCase):

    
    def setUp(self):

        self.auth = AuthService()
        self.events = EventService()
        self.db = Database()
        

        self.org_phone = "87770000001"
        self.auth.request_code(self.org_phone)
        code = self.db.get_verification_code(self.org_phone)["code"]
        self.org = self.auth.verify_code(self.org_phone, code)
        self.org_id = self.org["user_id"]

        self.user_phone = "87770000002"
        self.auth.request_code(self.user_phone)
        code = self.db.get_verification_code(self.user_phone)["code"]
        self.user = self.auth.verify_code(self.user_phone, code)
        self.user_id = self.user["user_id"]
    
    def test_1_create_event_success(self):

        print("\n Тест 1: Создание события")
        
        event_data = {
            "title": "Тестовое событие",
            "description": "Описание тестового события",
            "location": "Алматы",
            "lat": 43.2385,
            "lng": 76.9456,
            "date": "2026-03-25",
            "time": "15:00",
            "price": 0,
            "category": "Тест",
            "organizer_id": self.org_id
        }
        
        result = self.events.create_event(event_data)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Событие создано")
        self.assertIn("event_id", result)
        print(f"    Событие создано: {result['event_id']}")
    
    def test_2_create_event_without_title(self):
        """Тест 2: Создание события без названия"""
        print("\n Тест 2: Без названия")
        
        event_data = {
            "description": "Описание",
            "organizer_id": self.org_id
        }
        
        result = self.events.create_event(event_data)
        
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Укажите название")
        print(f"    Ошибка: {result['message']}")
    
    def test_3_register_for_event(self):
        """Тест 3: Запись на событие"""
        print("\n Тест 3: Запись на событие")

        event_data = {
            "title": "Событие для записи",
            "organizer_id": self.org_id
        }
        event_result = self.events.create_event(event_data)
        event_id = event_result["event_id"]

        result = self.db.register_for_event(event_id, self.user_id)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Вы записаны на событие!")
        print(f"    Запись успешна")
    
    def test_4_register_twice(self):
        """Тест 4: Двойная запись (не должна работать)"""
        print("\n Тест 4: Двойная запись")
        

        event_data = {
            "title": "Событие для двойной записи",
            "organizer_id": self.org_id
        }
        event_result = self.events.create_event(event_data)
        event_id = event_result["event_id"]

        self.db.register_for_event(event_id, self.user_id)

        result = self.db.register_for_event(event_id, self.user_id)
        
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Вы уже записаны")
        print(f"    Ошибка: {result['message']}")
    
    def test_5_get_all_events(self):
        """Тест 5: Получение всех событий"""
        print("\n Тест 5: Список событий")

        for i in range(3):
            event_data = {
                "title": f"Событие {i+1}",
                "organizer_id": self.org_id
            }
            self.events.create_event(event_data)
        
        events = self.events.get_all_events()
        
        self.assertGreaterEqual(len(events), 3)
        print(f"    Найдено событий: {len(events)}")
    
    def test_6_get_user_events(self):
        """Тест 6: Получение событий пользователя"""
        print("\n Тест 6: Мои события")
        
        event_data = {
            "title": "Событие для проверки",
            "organizer_id": self.org_id
        }
        event_result = self.events.create_event(event_data)
        event_id = event_result["event_id"]
        

        self.db.register_for_event(event_id, self.user_id)
        

        user_events = self.db.get_user_events(self.user_id)
        
        self.assertEqual(len(user_events), 1)
        self.assertEqual(user_events[0]["title"], "Событие для проверки")
        print(f"    Найдено записей: {len(user_events)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)