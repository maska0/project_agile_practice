from flask import Flask, request, jsonify
from flask_cors import CORS
from app.auth import AuthService
from app.events import EventService

app = Flask(__name__)
CORS(app)

auth_service = AuthService()
events_service = EventService()

@app.route('/api/request-code', methods=['POST'])
def request_code():
    data = request.json
    phone = data.get('phone')
    result = auth_service.request_code(phone)
    return jsonify(result)

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    phone = data.get('phone')
    code = data.get('code')
    result = auth_service.verify_code(phone, code)
    return jsonify(result)

@app.route('/api/create-event', methods=['POST'])
def create_event():
    data = request.json
    result = events_service.create_event(data)
    return jsonify(result)

@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events_service.get_all_events())

if __name__ == '__main__':
    print(" Запуск TAP бэкенда...")
    print(" Коды будут показываться в консоли")
    app.run(debug=True, port=5000)