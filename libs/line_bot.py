from flask import Flask
import requests
import os

app = Flask(__name__)

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
    user_id = 'U32ea1e57a98c99489ee1d238c0dfa78f'  # ここにメッセージを送りたいユーザーのIDを設定してください
    message_text = 'こんにちは、これはプッシュメッセージです！'
    status_code, response_text = send_push_message(token, user_id, message_text)
    return f'Status Code: {status_code}, Response: {response_text}'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9999)
