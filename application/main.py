#!/usr/bin/env python3

import os

from flask import Flask, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    mongo_client = MongoClient(os.environ['MONGO_URI'])
    database = mongo_client.chat

    while True:
        try:
            mongo_client.admin.command('ismaster')
        except ConnectionFailure:
            print("Mongo is not available, retrying...")
        else:
            break

    @app.route('/')
    def sessions():
        return render_template('session.html')

    @socketio.on('initialize')
    def handle_initialization(data):
        uid = data['uid']
        print(f"Started sending initial messages for {uid}")
        for document in database.messages.find({}):
            data = {
                'username': document['username'],
                'message': document['message']
            }
            socketio.emit(f'receive_message_{uid}', data)
            print("Sent", data)
        print("Finished sending initial messages")

    @socketio.on('send_message')
    def handle_message_sending(data):
        print('Received message: ', data)
        database.messages.insert_one(data.copy())
        socketio.emit('receive_message', data)

    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=8000)
