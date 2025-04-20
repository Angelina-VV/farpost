Проект: ETL-процесс для обработки данных форума
Описание проекта
Данный проект представляет собой автоматизированный процесс ETL (Извлечение, Преобразование, Загрузка), который извлекает данные из базы данных MySQL, обрабатывает их в соответствии с заданными алгоритмами и сохраняет в CSV-файл для дальнейшего использования.

Процесс включает три основных этапа:

Извлечение (Extract): Данные извлекаются из базы данных MySQL.
Преобразование (Transform): Данные проходят обработку в соответствии с заранее установленными алгоритмами.
Загрузка (Load): Обработанные данные сохраняются в файл формата CSV.
Установка и настройка Jenkins
1. Установка Jenkins
Для установки Jenkins на платформе macOS выполните следующие шаги:

Установите Jenkins с помощью Homebrew:
brew install jenkins-lts

Запустите службу Jenkins:
brew services start jenkins-lts

Откройте интерфейс Jenkins в браузере, перейдя по адресу: http://localhost:8080

2. Установка необходимых плагинов
После входа в Jenkins необходимо установить следующие плагины:

Git Plugin
Pipeline Plugin
3. Создание нового пользователя
Перейдите в раздел Manage Jenkins > Manage Users и создайте нового пользователя с правами администратора.

Настройка Jenkins Pipeline
1. Создание нового проекта
В Jenkins выполните следующие шаги:

Выберите New Item.
Введите название вашего проекта (например, "ETL Pipeline").
Выберите тип Pipeline и нажмите OK.

2. Настройка пайплайна
Добавьте следующий код пайплайна в раздел **Pipeline Script**:

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'START_DATE', defaultValue: '2025-04-01', description: 'Начальная дата (YYYY-MM-DD)')
        string(name: 'END_DATE', defaultValue: '2025-04-05', description: 'Конечная дата (YYYY-MM-DD)')
    }

    stages {
        stage('Клонируем репозиторий') {
            steps {
                git branch: '08.04.2025', url: 'https://github.com/Angelina-VV/farpost.git'
            }
        }

        stage('Запуск ETL (Python)') {
            steps {
                echo "Запускаем Python-скрипт с датами ${params.START_DATE} - ${params.END_DATE}"
                bat """
                echo ${params.START_DATE}>input.txt
                echo ${params.END_DATE}>>input.txt
                type input.txt | python3 aggregated_data.py
                """
            }
        }

        stage('Показать результат') {
            steps {
                echo "Содержимое aggregated_data.csv"
                bat 'type aggregated_data.csv || echo Файл не найден'
            }
        }
    }

    triggers {
        cron('0 2 * * *') // каждый день в 5:00 
    }
}
