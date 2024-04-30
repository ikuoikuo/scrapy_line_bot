import requests

def call_send_message():
    # Flask アプリケーションが実行されているアドレス
    url = 'http://localhost:9999/send_message'
    try:
        # GET リクエストを送信
        response = requests.get(url)
        print(f'Status Code: {response.status_code}')
        print(f'Response Body: {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    call_send_message()
    