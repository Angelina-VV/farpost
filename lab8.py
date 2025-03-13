import sqlite3
from collections.abc import Collection

class TableData(Collection):

    def __init__(self, database_name: str, table_name: str):
        """
        Инициализирует TableData с именем базы данных и именем таблицы.

        Args:
            database_name: Имя файла базы данных SQLite3.
            table_name: Имя таблицы, которую нужно обернуть.
        """
        self.database_name = database_name
        self.table_name = table_name

    def __len__(self) -> int:
   
       # Возвращает количество строк в таблице.
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                # Проверяем существование таблицы
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';")
                if cursor.fetchone() is None:
                    raise ValueError(f"Таблица '{self.table_name}' не существует.")
                
                # Безопасная конкатенация строк для имени таблицы
                query = f'SELECT count(*) FROM "{self.table_name}"'  # Добавляем двойные кавычки
                cursor.execute(query)
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return 0  

    def __contains__(self, item: str) -> bool:

        #  Проверяет, существует ли запись с указанным именем в таблице.
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                query = f'SELECT 1 FROM "{self.table_name}" WHERE name = :name' # Добавляем двойные кавычки
                cursor.execute(query, {'name': item})
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False

    def __getitem__(self, key: str) -> tuple:

        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                query = f'SELECT * FROM "{self.table_name}" WHERE name = :name' # Добавляем двойные кавычки
                cursor.execute(query, {'name': key})
                row = cursor.fetchone()
                if row is None:
                    raise KeyError(f"Запись с именем '{key}' не найдена в таблице '{self.table_name}'.")
                return row
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            raise KeyError(f"Ошибка при получении записи '{key}': {e}")

    
    def __iter__(self):
        """
        Возвращает итератор по строкам таблицы, отсортированным по имени.
        """
        try:
            with sqlite3.connect(self.database_name) as conn:
                cursor = conn.cursor()
                query = f'SELECT * FROM "{self.table_name}" ORDER BY name' # Добавляем двойные кавычки
                cursor.execute(query)
                while row := cursor.fetchone():
                    yield row
        except sqlite3.Error as e:
            print(f"Ошибка при итерации по таблице: {e}")
            return  # Или raise, в зависимости от желаемого поведения

if __name__ == '__main__':
    presidents = TableData('d:\example.sqlite', 'presidents')

    print(f"Количество президентов: {len(presidents)}")
    print(f"Существует ли Ельцин: {'Yeltsin' in presidents}")
    try:
        yeltsin = presidents['Yeltsin']
        print(f"Данные о Ельцине: {yeltsin}")
    except KeyError as e:
        print(e)

    print("Имена всех президентов:")
    for president in presidents:
        print(president[0])  # Предполагается, что имя находится в первом столбце
