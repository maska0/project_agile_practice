import unittest
import sys
import os
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import AuthService
from database import Database

class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.auth = AuthService()
        self.db = Database()
        self.test_phone = "87770000000"
        

        self.db.delete_verification_code(self.test_phone)
    
    def test_1_request_code_success(self):
        """Тест 1: Успешный запрос кода"""
        print("\n Тест 1: Запрос кода")
        
        result = self.auth.request_code(self.test_phone)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Код отправлен")
        

        stored = self.db.get_verification_code(self.test_phone)
        self.assertIsNotNone(stored)
        print(f"    Код создан: {stored['code']}")
    
    def test_2_request_code_invalid_phone(self):
        """Тест 2: Запрос кода с неверным номером"""
        print("\n Тест 2: Неверный номер")
        
        result = self.auth.request_code("123")  
        
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Неверный номер")
        print(f"    Ошибка: {result['message']}")
    
    def test_3_verify_code_success(self):
        """Тест 3: Успешное подтверждение кода"""
        print("\n Тест 3: Подтверждение кода")
        

        self.auth.request_code(self.test_phone)
        stored = self.db.get_verification_code(self.test_phone)
        code = stored["code"]
        

        result = self.auth.verify_code(self.test_phone, code)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Регистрация успешна")
        self.assertIn("user_id", result)
        print(f"    Пользователь создан: {result['user_id']}")
    
    def test_4_verify_code_wrong(self):
        """Тест 4: Неверный код"""
        print("\n Тест 4: Неверный код")
        
        self.auth.request_code(self.test_phone)
        
        result = self.auth.verify_code(self.test_phone, "000000")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Неверный код")
        print(f"    Ошибка: {result['message']}")
    
    def test_5_verify_code_expired(self):
        """Тест 5: Просроченный код"""
        print("\n Тест 5: Просроченный код")
    
        self.auth.request_code(self.test_phone)
        

        import time
        expired_time = time.time() - 1 

        code = self.db.get_verification_code(self.test_phone)["code"]
        self.db.save_verification_code(self.test_phone, code, expired_time)
        
        result = self.auth.verify_code(self.test_phone, code)
        
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Код истек")
        print(f"    Ошибка: {result['message']}")
    
    def test_6_verify_without_request(self):
        """Тест 6: Подтверждение без запроса кода"""
        print("\n Тест 6: Без запроса кода")
        
        result = self.auth.verify_code(self.test_phone, "123456")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Сначала запросите код")
        print(f"    Ошибка: {result['message']}")

if __name__ == '__main__':
    unittest.main(verbosity=2)