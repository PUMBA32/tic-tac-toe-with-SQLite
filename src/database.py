import sqlite3
from typing import List, Any, Dict, Optional


class Database:
    def __init__(self) -> None:
        self.__PATH_TO_DB: str = "D:\\Coding\\PYTHON\\webdev\\sqlite\\tic_tac_toe_with_db\\database\\data.db"
        
        # Подключение к базе данных
        with sqlite3.connect(self.__PATH_TO_DB) as self.con:
            self.cur = self.con.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                             user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT,
                             password TEXT,
                             wins INTEGER DEFAULT 0,
                             losses INTEGER DEFAULT 0
                             )""")
            self.con.commit()


    def get_all_player(self) -> List[Any]:
        '''Получение списка всех пользователей из базы данных'''

        try:
            self.cur.execute("SELECT * FROM users")
        except Exception as ex:
            print(f"Ошибка получения списка всех игроков: {ex}\n")
        
        return self.cur.fetchall()


    def get_top_3(self) -> List[Any]:
        '''Получение списка из 3х лучших игроков из базы данных'''
        
        try:
            self.cur.execute("SELECT name, wins, losses FROM users ORDER BY wins DESC LIMIT 3")
        except Exception as ex:
            print(f"Ошибка получения 3 лучших игроков: {ex}\n")

        return self.cur.fetchall()


    def get_stats_by_name(self, name: str) -> Optional[Dict[str, int]]:
        '''Получение статистики игрока по его имени'''
        
        if name == None:
            print("Ошибка! Вы ввели пустое имя\n")
            return None 

        try:
            self.cur.execute("SELECT wins, losses FROM users WHERE name=?", (name,))
            result = self.cur.fetchone()
        except Exception as ex:
            print(f"Ошибка получения данных по имени игрока: {ex}\n")

        return {"wins": result[0], "losses": result[1]} if result else None


    def get_names_and_passwords(self) -> List[Any]:
        '''Получение списка всех имен и паролей от аккаунтов у игроков'''

        self.cur.execute("SELECT name, password FROM users")
        return self.cur.fetchall()
    

    def add_new_user(self, name: str, password: str) -> None:
        '''Добавление нового пользователя в базу данных'''
        try:
            self.cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
            self.con.commit()
        except Exception as ex:
            print(f"Ошибка добавления нового пользователя: {ex}\n")
        else:
            print("Новый пользователь успешно добавлен!\n")


    def update_data_by_name(self, name: str, wins: int, losses: int) -> Optional[ValueError]:
        '''Обновление статистики пользователя по его имени'''
        
        # Проверка на корректность данных wins и losses
        if type(wins) != int or type(losses) != int or name != str:
            raise ValueError

        try: 
            self.cur.execute("UPDATE users SET wins=?, losses=? WHERE name=?", (wins, losses, name))
            self.con.commit()
        except Exception as ex:
            print(f"Ошибка обновления данных о проигрышах и победах пользователя {name}: {ex}\n")
        else: 
            print("Данные УСПЕШНО обновлены!\n")
        

    def close_db(self) -> None:
        '''Закрытие базы данных'''

        self.con.close()
