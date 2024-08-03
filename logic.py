import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE users (
                            user_id INTEGER,
                            user_name TEXT PRIMARY KEY,
                            problem TEXT NOT NULL,
                            status TEXT,
                            contact_info TEXT
                        )''')
            conn.execute('''CREATE TABLE description (
                            user_id INTEGER,
                            problem TEXT,
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
        
    def insert_problem(self, data):
        sql = 'INSERT INTO users (user_id, user_name, problem, status, contact_info) values(?, ?, ?, ?, ?)'
        self.__executemany(sql, [data])

    def get_participance(self, user_id):
        return self.__select_data(sql='SELECT * FROM users WHERE user_id = ?', data = (user_id,))
    
    def get_participants(self, dat):
        return self.__select_data(sql='SELECT * from users WHERE problem = ?', data = (dat,))
    
    def get_participant_cert(self, dat):
        return self.__select_data(sql='SELECT * from users WHERE user_name = ?', data = (dat,))

    # def get_name(self,  user_id):
    #     return self.__select_data(sql='SELECT user_name FROM users WHERE user_id = ?', data = (user_id,))
    
    def insert_deets(self, data):
        sql = 'INSERT INTO description (user_id, problem, detailed_desc) values(?, ?, ?)'
        self.__executemany(sql, [data])
    
    def get_deets(self, user_id):
        return self.__select_data(sql='SELECT * FROM description WHERE problem = ?', data = (user_id,))

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    #manager.default_insert()

    