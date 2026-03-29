import time
import random
from database import Database

class AuthService:
    def __init__(self):
        self.db = Database()
    
    def request_code(self, phone):
        if not phone or len(phone) < 10:
            return {"success": False, "message": "Неверный номер"}
        
        code = str(random.randint(100000, 999999))
        expires_at = time.time() + 300 
        
        self.db.save_verification_code(phone, code, expires_at)
        print(f" Код для {phone}: {code}")  
        
        return {"success": True, "message": "Код отправлен"}
    
    def verify_code(self, phone, code):
        stored = self.db.get_verification_code(phone)
        if not stored:
            return {"success": False, "message": "Сначала запросите код"}
        if time.time() > stored["expires_at"]:
            self.db.delete_verification_code(phone)
            return {"success": False, "message": "Код истек"}
        if stored["code"] != code:
            return {"success": False, "message": "Неверный код"}
        user = self.db.create_user(phone)
        self.db.delete_verification_code(phone)
        
        return {
            "success": True,
            "message": "Регистрация успешна",
            "user_id": user["id"]
        }