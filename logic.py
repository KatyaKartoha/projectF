import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE users (
                            user_id INTEGER PRIMARY KEY
                            user_name TEXT,
                            problem TEXT NOT NULL,
                            status TEXT,
                            contact_info TEXT,
                            problem_id INTEGER,
                            FOREIGN KEY(problem_id) REFERENCES description(problem_id)
                        )''')
            conn.execute('''CREATE TABLE description (
                            problem_id INTEGER PRIMARY KEY,
                            detailed_desc TEXT
                        )''')
            conn.commit()
        print("База данных успешно создана.")

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def insert_con_d(self, data):
        sql = 'INSERT INTO users (user_id, user_name, problem, status, contact_info, problem_id) values(?, ?, ?, ?, ?, ?)'
        self.__executemany(sql, [data])

    def get_participance(self, user_id):
        return self.__select_data(sql='SELECT * FROM users WHERE user_id = ?', data = (user_id,))
    


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()