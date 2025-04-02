import mysql.connector
import time
from datetime import datetime
import os
from clickhouse_driver import Client

# Настройки подключения к базе данных MySQL
mysql_config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "mydatabase",
}

# Настройки подключения к ClickHouse
clickhouse_client = Client(host='localhost')

def fetch_data():
    # Подключение к базе данных MySQL
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT * FROM messages")  # Запрос к таблице messages
    data = cursor.fetchall()

    # Закрытие соединения
    cursor.close()
    conn.close()

    return data


def insert_into_clickhouse(data):
    if not data:
        print("Нет данных для вставки.")
        return

    # Вставка данных в ClickHouse
    clickhouse_client.execute(
        "INSERT INTO messages (id, export_timestamp, message) VALUES",
        data
    )
    print(f"Вставлено {len(data)} строк в ClickHouse.")


if __name__ == "__main__":
    while True:
        data = fetch_data()
        insert_into_clickhouse(data)
        time.sleep(300)  # 5 минут
