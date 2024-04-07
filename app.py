from flask import Flask, render_template, request, jsonify
from models import ChatHistory, engine
from views import chat
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat)

if __name__ == '__main__':
    app.run(debug=True)