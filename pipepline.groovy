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