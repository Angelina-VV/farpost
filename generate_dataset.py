import random
import mysql.connector
from datetime import datetime, timedelta
from faker import Faker

# Создаем экземпляр Faker для генерации случайных данных
fake = Faker()

# Подключаемся к базе данных MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydb"
)

cursor = db.cursor()

# Генерация случайного времени в пределах одного месяца
def random_date(start_date, end_date):
    return start_date + timedelta(minutes=random.randint(0, int((end_date - start_date).total_seconds() / 60)))

# Генерация случайных пользователей
def generate_and_insert_users(num_users):
    users = []
    for _ in range(num_users):
        is_logged_in = random.choice([0, 1])  # 0 - не залогинен, 1 - залогинен
        user = {
            "username": fake.user_name(),
            "password": fake.password() if is_logged_in == 1 else None,  # Если пользователь залогинен, генерируем пароль
            "is_logged_in": is_logged_in
        }
        
        # Генерация даты регистрации только для залогиненных пользователей
        registration_date = random_date(datetime(2025, 4, 1), datetime(2025, 4, 30))

        # Вставляем пользователя в таблицу users
        cursor.execute(""" 
            INSERT INTO users (username, password, is_logged_in) 
            VALUES (%s, %s, %s)
        """, (user["username"], user["password"], user["is_logged_in"]))
        db.commit()

        # Получаем ID нового пользователя
        user_id = cursor.lastrowid
        users.append((user_id, registration_date))  # Храним ID пользователя и дату регистрации

        # Записываем в таблицу actions
        if user["is_logged_in"] == 1:
            cursor.execute(""" 
                INSERT INTO actions (a_user_id, action_type, response, action_time) 
                VALUES (%s, 'registration', 'success', %s)
            """, (user_id, registration_date))
        else:
            cursor.execute(""" 
                INSERT INTO actions (a_user_id, action_type, response, action_time) 
                VALUES (%s, 'login_without_registration', 'success', %s)
            """, (user_id, registration_date))
        db.commit()

    return users

# Генерация случайных тем
def generate_and_insert_topics(num_topics, users, start_date, end_date):
    topics = []
    for _ in range(num_topics):
        topic_title = fake.sentence()
        created_at = random_date(start_date, end_date)  # Генерируем случайную дату в пределах месяца

        # Выбираем случайного пользователя для привязки к теме
        user_id = random.choice(users)[0]
        
        cursor.execute("""
            INSERT INTO topics (title, user_id, created_at)
            VALUES (%s, %s, %s)
        """, (topic_title, user_id, created_at))
        db.commit()

        # Получаем ID новой темы
        topic_id = cursor.lastrowid
        topics.append(topic_id)
    return topics

# Генерация сообщений
def generate_and_insert_messages(user_id, topic_id, action_date):
    content = fake.text()
    cursor.execute("""
        INSERT INTO messages (m_user_id, m_topic_id, content, created_at)
        VALUES (%s, %s, %s, %s)
    """, (user_id, topic_id, content, action_date))
    db.commit()

    message_id = cursor.lastrowid
    return message_id

# Генерация действий
def generate_action(user_id, action_date, login_status, topic_id=None, message_id=None):
    action_type = "no_action"  # Устанавливаем значение по умолчанию для action_type
    response = "success"

    # Действие "create_topic"
    if random.random() < 0.5:  # 50% шанс на создание темы
        if login_status == 1:
            action_type = "create_topic"
            response = "success"
        else:
            action_type = "create_topic"
            response = "error: no login"
            topic_id = None  # Не создаем тему, если ошибка

    # Действие "write_message"
    if random.random() < 0.5:  # 50% шанс на создание сообщения
        action_type = "write_message"
        if random.random() < 0.5:  # 50% сообщений от незалогиненных пользователей
            message_id = None  # Сообщение анонимное
            response = "success"
        else:
            if topic_id is None:
                topic_id = 1  # Иначе выберем существующую тему (например, 1)

            # Генерация сообщения и вставка в таблицу messages
            message_id = generate_and_insert_messages(user_id, topic_id, action_date)
            response = "success"  # Сообщение от залогиненного пользователя

    # Логирование действия в таблицу actions
    cursor.execute("""
        INSERT INTO actions (a_user_id, action_type, response, action_time, topic_id, message_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, action_type, response, action_date, topic_id, message_id))
    db.commit()

# Генерация данных для пользователей, тем, сообщений и действий за месяц
def generate_data_for_month(start_date, end_date):
    # Сначала генерируем пользователей
    users = generate_and_insert_users(10)  # Генерация и вставка 10 пользователей
    
    # Генерация тем
    topics = generate_and_insert_topics(5, users, start_date, end_date)  # Генерация 5 тем с привязкой к пользователям

    # Затем генерируем действия за каждый день месяца
    current_date = start_date
    while current_date <= end_date:
        for user_id, registration_date in users:
            login_status = random.choice([0, 1])  # Симуляция случайного состояния логина
            topic_id = random.choice(topics) if login_status == 1 else None  # Генерация темы, если залогинен
            message_id = None  # Изначально message_id будет None, потом оно будет заменено на реальный id
            generate_action(user_id, current_date, login_status, topic_id, message_id)
        current_date += timedelta(days=1)

# Установим диапазон дат для одного месяца
start_date = datetime(2025, 4, 1)
end_date = datetime(2025, 4, 30)

# Генерация данных
generate_data_for_month(start_date, end_date)

# Закрываем соединение с базой данных
cursor.close()
db.close()
