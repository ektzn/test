import cx_Oracle
import csv
from datetime import datetime
import json

# Функция получения данных для подключения
def get_credentials(file):
    with open('credentials.json') as f:
        creds = json.load(f)
        return creds.get(file)

# Выполнение основной задачи
def main():
    # Установка параметров подключения
    creds = get_credentials('test1')
    username = creds['username']
    password = creds['password']
    dsn = creds['dsn']

    # Подключение к базе данных
    connection = cx_Oracle.connect(username, password, dsn)

    # Создание курсора
    cursor = connection.cursor()

    # Выполнение SQL-запроса
    query = '''
        SELECT cl.first_name, cl.last_name, cr.credit_number 
        FROM client cl
        JOIN relation r
        ON cl.id = r.client
        JOIN credit cr
        ON r.credit = cr.id
        WHERE cr.balance > 1000
    '''
    cursor.execute(query)

    # Извлечение всех результатов
    rows = cursor.fetchall()

    # Определение названий столбцов
    columns = [col[0] for col in cursor.description]

    # Получение текущей даты
    current_date = datetime.now().strftime("%d.%m.%Y")

    # Определение имени файла с текущей датой
    file_name = f'report_{current_date}.csv'

    # Запись данных в CSV-файл
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Данные успешно записаны в файл: {file_name}")

    # Закрытие курсора и соединения
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()