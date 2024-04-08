import requests
import time
from models import ChatHistory, Session
from flask import Blueprint, jsonify, request
from datetime import datetime
import re
MAX_ATTEMPTS = 50

chat = Blueprint('chat', __name__)

@chat.route('/chat', methods=['POST'])
def chat_route():
    user_input = request.json.get('user_input')
    execution_time_start = time.time()
    
    if user_input.isdigit() and 1 <= int(user_input) <= 8:
        images = get_dog_images(int(user_input))
        breeds = [re.search('breeds/(.*?)/', url).group(1) for url in images]
        execution_time = time.time() - execution_time_start
        save_chat_history(user_input, execution_time, True, images)
        return jsonify({'images': images, 'breeds': breeds, 'status': 'success'})
    else:
        execution_time = time.time() - execution_time_start
        save_chat_history(user_input, execution_time, False, 'Please introduce any number between 1 and 8')
        return jsonify({'message': 'Please introduce any number between 1 and 8', 'status': 'error'})

def get_dog_images(count):
    breeds = set()
    urls = []
    attempts = 0
    while len(urls) < count and attempts < MAX_ATTEMPTS:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code == 200:
            image_url = response.json()['message']
            breed = re.search('breeds/(.*?)/', image_url).group(1)
            if breed not in breeds:
                breeds.add(breed)
                urls.append(image_url)
        attempts += 1
    return urls

def save_chat_history(user_input, execution_time, is_valid, result):
    chat_history = ChatHistory(
        user_input=user_input,
        execution_time=execution_time,
        is_valid_input=is_valid,
        result=result,
        timestamp=datetime.utcnow()
    )
    session = Session()
    session.add(chat_history) 
    session.commit() 
    session.close() 

@chat.route('/history', methods=['GET'])
def chat_history():
    session = Session()
    history = session.query(ChatHistory).all()
    session.close()
    history_with_breeds = []
    for h in history:
        breeds = []
        images = []
        history_entry = {}
        if h.is_valid_input:
            images = h.result.strip("{}").split(",")
            breeds = [re.search('breeds/(.*?)/', url).group(1) for url in images if re.search('breeds/(.*?)/', url)]
            history_entry = {
            'user_input': h.user_input,
            'execution_time': h.execution_time,
            'is_valid_input': h.is_valid_input,
            'timestamp': h.timestamp.isoformat(),
            'images': images,
            'breeds': breeds
        }
        else:
            history_entry = {
            'user_input': h.user_input,
            'execution_time': h.execution_time,
            'is_valid_input': h.is_valid_input,
            'text': h.result,
            'timestamp': h.timestamp.isoformat(), 
        }
        history_with_breeds.append(history_entry)
    return jsonify(history_with_breeds)

