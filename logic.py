import sqlite3
from config import DATABASE, TOKEN

class DatabaseManager:
    def __init__(self, db_name: str = DATABASE):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row

    def create_table(self, table_name: str, schema: str):
        if not table_name.isidentifier():
            raise ValueError(f"Недопустимое имя таблицы: {table_name}")
            
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {schema}
        )
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(query)
                print(f"Таблица '{table_name}' успешно создана")
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")
    
    def fill_table(self, tablename: str, data: list, columns: str = None):
        """
        Заполняет таблицу данными
        
        :param tablename: Имя таблицы
        :param data: Список кортежей с данными
        :param columns: Опционально - имена колонок в формате "(col1, col2)"
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                placeholders = ", ".join(["?"] * len(data[0]))
                cols = f"({columns}) " if columns else ""
                
                cursor.executemany(
                    f"INSERT OR IGNORE INTO {tablename} {cols}VALUES ({placeholders})",
                    data
                )
                print(f"Добавлено {cursor.rowcount} записей в таблицу '{tablename}'")
        except sqlite3.Error as e:
            print(f"Ошибка при заполнении таблицы: {e}")



if __name__ == '__main__':
    manager = DatabaseManager()
    #Закоментировано, т.к. таблицы уже есть
    '''
    manager.create_table(  
        table_name="projects",
        schema="""
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    project_name TEXT NOT NULL,
    description TEXT,
    url TEXT UNIQUE,
    skill_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY(status_id) REFERENCES status(status_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
    """
    )
    '''

    status_data = [
        (0, "Проектирование"),
        (1, "В процессе разработки"),
        (2, "Разработан"),
        (3, "Поддерживается/обновляется"),
        (4, "Приостановлен/Заморожен"),
        (5, "Закончен/Не поддерживается"),   
    ]

    manager.fill_table(
        tablename="status",
        data=status_data,
        columns="status_id, name"
    )

    status_data = [
        (0, "До начала курса", "Python"),
        (1, "с начала 1 курса", "Telegram"),
        (2, "С начала 3 курса", "SQL"),
        (3, "К концу 1 курса", "API"),
        (4, "К концу 1 курса", "HTML"),
        (5, "Еще не изучен", "CSS"),
        (6, "Еще не изучен", "FLASK"),
        (7, "Еще не изучен", "AI")
    ]

    manager.fill_table(
        tablename="skills",
        data=status_data,
        columns="skill_id, date, skill_name"
    )

    projects_data = [
        (0, -37, "pokbot",
         """Ну, я просто пытаюсь хоть что-то сделать. Пока что это не рабочий бот а только наброски...""",
         "https://github.com/Cutey-Whity1/pokbot.git",
         1, 4),
        
        (1, -37, "new_some_bot",
         "None",
         "https://github.com/Cutey-Whity1/new_some_bot.git",
         1, 4),
         
        (2, -37, "portfolio",
         """Portfolio mine portfolio-botie :3""",
         "https://github.com/Cutey-Whity1/Portfolio.git",
         2, 3)
    ]
    
    manager.fill_table(
        tablename="projects",
        data=projects_data,
        columns="project_id, user_id, project_name, description, url, skill_id, status_id"
    )
