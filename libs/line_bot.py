from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
def load_user_ids(file_path):
    """ ファイルからユーザーIDを読み込む """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def send_push_message(token, user_id, message_text):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        'to': user_id,
        'messages': [{
            'type': 'text',
            'text': message_text
        }]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

@app.route("/send_message")
def send_message():
    token =  os.getenv('CHANNEL_ACCESS_TOKEN') 
    user_ids = load_user_ids('../aidb_scrapy/users.csv')
    message_text = request.args.get('message', 'こんにちは、これはプッシュメッセージです！') 
    results = []
    for user_id in user_ids:
        status_code, response_text = send_push_message(token, user_id, message_text)
        results.append({'user_id': user_id, 'Status Code': status_code, 'Response': response_text})
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9999)
