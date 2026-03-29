import math
from database import Database

class EventService:
    def __init__(self):
        self.db = Database()
    
    def create_event(self, data):
        if not data.get("title"):
            return {"success": False, "message": "Укажите название"}
        if not data.get("organizer_id"):
            return {"success": False, "message": "Не указан организатор"}
        event_id = self.db.create_event(data)
        if event_id:
            return {
                "success": True,
                "message": "Событие создано",
                "event_id": event_id
            }
        return {"success": False, "message": "Ошибка создания"}
    
    def get_all_events(self):
        return self.db.get_all_events()