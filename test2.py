import requests
import json

# Эндпоинт для авторизации
LOGIN_URL = 'https://reqres.in/api/login'

# Функция получения данных для авторизации
def get_credentials(file):
    with open('credentials.json') as f:
        creds = json.load(f)
        return creds.get(file)

# Функция для авторизации и получения токена
def login():
    login_data = get_credentials('test2')
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        return None

# Пример использования токена для выполнения защищенного запроса
def get_protected_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get('https://reqres.in/api/users', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        return None

def main():
    token = login()
    if token:
        print(f"Получен токен: {token}")
        protected_data = get_protected_data(token)
        if protected_data:
            print("Защищенные данные:")
            print(json.dumps(protected_data, indent=4))

if __name__ == '__main__':
    main()