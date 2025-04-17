import mysql.connector
import csv
from datetime import datetime, timedelta

# Подключение к базе данных MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)

cursor = db.cursor()

# Функция для агрегации данных по дням
def aggregate_data(start_date, end_date):
    # Инициализируем переменные
    daily_data = []

    # Итерируем по дням в заданном периоде
    current_date = start_date
    while current_date <= end_date:
        # 1. Количество новых аккаунтов
        cursor.execute("""
            SELECT COUNT(*) FROM actions 
            WHERE action_type = 'registration' 
            AND DATE(action_time) = %s
        """, (current_date.date(),))
        new_accounts = cursor.fetchone()[0]

        # 2. Количество сообщений, написанных анонимами
        cursor.execute("""
            SELECT COUNT(*) FROM actions 
            WHERE action_type = 'write_message' 
            AND response = 'success' 
            AND message_id IS NULL 
            AND DATE(action_time) = %s
        """, (current_date.date(),))
        anonymous_messages = cursor.fetchone()[0]

        # Общее количество сообщений за день
        cursor.execute("""
            SELECT COUNT(*) FROM actions 
            WHERE action_type = 'write_message' 
            AND response = 'success' 
            AND DATE(action_time) = %s
        """, (current_date.date(),))
        total_messages = cursor.fetchone()[0]

        # 3. Процент анонимных сообщений от всех сообщений
        if total_messages > 0:
            anonymous_percentage = (anonymous_messages / total_messages) * 100
        else:
            anonymous_percentage = 0

        # 4. Процентное изменение количества тем по сравнению с предыдущим днем
        cursor.execute("""
            SELECT COUNT(*) FROM topics 
            WHERE DATE(created_at) = %s
        """, (current_date.date(),))
        topics_today = cursor.fetchone()[0]

        if current_date > start_date:
            cursor.execute("""
                SELECT COUNT(*) FROM topics 
                WHERE DATE(created_at) = %s
            """, (current_date - timedelta(days=1),))
            topics_yesterday = cursor.fetchone()[0]

            if topics_yesterday > 0:
                topic_growth_percentage = ((topics_today - topics_yesterday) / topics_yesterday) * 100
            else:
                topic_growth_percentage = 0
        else:
            topic_growth_percentage = 0  # Нет данных за предыдущий день для первого дня

        # Добавляем агрегацию для текущего дня в список
        daily_data.append([
            current_date.strftime('%Y-%m-%d'),
            new_accounts,
            anonymous_percentage,
            total_messages,
            topic_growth_percentage
        ])

        # Переходим к следующему дню
        current_date += timedelta(days=1)

    return daily_data

# Функция для записи данных в CSV файл
def write_to_csv(data, filename="aggregated_data.csv"):
    header = ["day", "new_accounts", "anonymous_percentage", "total_messages", "topic_growth_percentage"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

# Функция для получения даты в формате YYYY-MM-DD
def get_date_from_input(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

# Получаем дату начала и конца периода для агрегации
start_date_str = input("Введите начальную дату в формате YYYY-MM-DD: ")
end_date_str = input("Введите конечную дату в формате YYYY-MM-DD: ")

start_date = get_date_from_input(start_date_str)
end_date = get_date_from_input(end_date_str)

# Получаем агрегацию данных
aggregated_data = aggregate_data(start_date, end_date)

# Записываем результат в CSV файл
write_to_csv(aggregated_data)

# Закрытие соединения с базой данных
cursor.close()
db.close()

print("Агрегация данных завершена и сохранена в файл aggregated_data.csv")
