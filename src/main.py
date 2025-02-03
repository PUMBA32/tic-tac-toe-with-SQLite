import os
import sys

from game import Game
from database import Database

from typing import Dict, Optional


class Menu:
    def __init__(self) -> None:
        self.first_menu: tuple[str] = (
            "login",
            "register",
            "exit"
        )
        self.second_menu: tuple[str] = (
            "start game",
            "all players",
            "best players",
            "personal statistic",
            "exit"
        )
        self.db: Database = Database()
    

    def __clear_console(self) -> None:
        '''Очищает консоль'''
        os.system("cls" if sys.platform == 'win32' else "clear")

    
    def __get_data_from_user(self) -> tuple[str]:
        '''Получение имени и пароля от пользователя'''
        self.__clear_console()

        while True:
            name: str = input("enter name: ").strip()
            if len(name) == 0:
                self.__clear_console()
                print("Error! This field should't be empty\n")
                continue

            password: str = input("enter password: ").strip()
            if len(password) == 0:
                self.__clear_console()
                print("Error! This field should't be empty\n")
                continue
            break
        
        return (name, password)
    
    
    def __start_game(self) -> None:
        # Получение статистики игрока по имени
        stats: Dict[str, int] = self.db.get_stats_by_name(self.name)
        wins = stats['wins']
        losses = stats['losses']

        # Начало и конец игры с последующим получением новой статистики
        game = Game(wins, losses)
        wins, losses = game.start()

        # Обновление данных об игроке в базе данных по его имени
        self.db.update_data_by_name(self.name, wins, losses)

    
    def __show_all_players(self) -> None:
        self.__clear_console()
        print("Statistic by all players:\n  ")

        # Получение данных по всем игрокам из базы данных
        players = self.db.get_all_player()

        for player in players:
            print(f'- {player[1]}; wins: {player[3]}; losses: {player[4]}')
        input("\nEnter any key to turn back >>> ")


    def __show_best_players(self) -> None:
        self.__clear_console()
        
        # Получение данных по 3м лучшим игрокам из базы данных
        players = self.db.get_top_3()

        for i, player in enumerate(players):
            print(f'{i+1}. {player[0]}; wins: {player[1]}; losses: {player[2]}')
        input("\nEnter any key to turn back >>> ")

    
    def __show_personal_statistic(self) -> None:
        self.__clear_console()

        # Получение данных об игроке по его имени
        data = self.db.get_stats_by_name(self.name)

        if data != None:
            print(f'Wins: {data['wins']}')
            print(f'Losses: {data['losses']}')

            all_games: int = int(data['wins']) + int(data['losses'])
            print(f'All games: {all_games}\n')
            
            input("\nEnter any key to turn back >>> ")


    def show_menu(self, menu_type: int = 1) -> Optional[ValueError]:
        self.__clear_console()

        if type(menu_type) != int: raise ValueError

        for i, el in enumerate(self.first_menu if menu_type == 1 else self.second_menu):
            print(f"[{i+1}] - {el}")
        print()


    def login(self) -> None:
        self.name, password = self.__get_data_from_user()  # Получение данных аккаунта от пользователя
        users = self.db.get_names_and_passwords()  # Получение списка всех имен и паролей из базы данных

        # Проверка существует ли пользователь с таким ником и паролем в базе данных
        for user in users:
            if user[0] == self.name and user[1] == password:
                break
        else:  # Если такого пользователя нету
            self.__clear_console()  # Очистка консоли
            print("There is no such user! Maybe you gotta create a new profile.\n")
            return
        
        # Если такой пользователь существует, то запускается игровое меню
        self.start_second_menu()


    def register(self) -> None:
        self.name, password = self.__get_data_from_user()  # Получение вводных данных от пользователя
        users = self.db.get_names_and_passwords()  # получение всех имен и паролей из базы данных

        for user in users:
            if user[0] == self.name:
                print("This name already occupied! Try another name.\n") 
                return
        else:
            self.db.add_new_user(self.name, password)

            # Если пользователь успешно добавлен, то запускается игровое меню
            self.start_second_menu()


    def start_second_menu(self) -> None:
        while True:
            self.show_menu(menu_type=2)
            choice: str = input(">>> ").strip()

            match choice:
                case "1": self.__start_game()
                case "2": self.__show_all_players()
                case "3": self.__show_best_players()
                case "4": self.__show_personal_statistic()
                case _: 
                    self.db.close_db()
                    return


def main() -> None:
    while True:
        menu: Menu = Menu()
        menu.show_menu()
        first_ch: str = input(">>> ").strip()

        if first_ch == "1": menu.login()
        elif first_ch == "2": menu.register()
        else: break


if __name__ == '__main__':
    main()