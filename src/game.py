import os
import sys

from random import randint
from typing import List, Tuple, Optional


class Game:
    def __init__(self, wins: int = 0, losses: int = 0) -> None:
        self.g_m: List[int] = [
            1,2,3,
            4,5,6,
            7,8,9
        ]
        self.wins: int = wins
        self.losses: int = losses


    def __clear_console(self) -> None:
        '''Очищает консоль'''

        os.system("cls" if sys.platform == 'win32' else "clear")


    def show_map(self) -> None:
        '''Выводит игровую карту'''

        print("=============", end="")
        for i, el in enumerate(self.g_m):
            if i % 3 == 0: print() 
            print("|", end="")
            
            if el == -1: print(f" X ", end="")
            elif el == -2: print(f" O ", end="")
            else: print(f" {el} ", end="")

            if i+1 in (3,6,9): print("|\n=============", end="")
        print("\n")


    def user_step(self) -> None:
        '''Выполнение хода игрока'''

        while True:
            try:
                index: int = int(input("index of cell >>> "))
            except ValueError as ex:
                print(f"Error! You gotta enter the NUMBER: {ex}")
            else:
                if 1 <= index <= 9 and self.g_m[index-1] not in (-1, -2):
                    self.g_m[index-1] = -2
                    self.__clear_console()
                    print("Game map after YOUR step:")
                    self.show_map()
                    break
                else: 
                    print("Error! This cell already occupied or invalid index!") 

    
    def bot_step(self) -> None:
        '''Выполнение хода компьютера'''
         
        self.__clear_console()
        while True:
            index: int = randint(0, 8)
            if self.g_m[index-1] not in (-1, -2):
                self.g_m[index-1] = -1
                break
        print("Game map after COMPUTER step:")
        self.show_map()

    
    def who_winner(self) -> Optional[int]:
        '''Проверка всей карты на наличие победителя или ничьи'''

        winning_combo: List[Tuple[int]] = [
            (0,1,2), (3,4,5), (6,7,8),  # Горизонтальные
            (0,3,6), (1,4,7), (2,5,8),  # Вертикальные полосы
            (0,4,8), (2,4,5)            # Диагонали
        ]

        # Победил либо игрок, либо компьютер
        for combo in winning_combo:
            if self.g_m[combo[0]] == self.g_m[combo[1]] == self.g_m[combo[2]]:
                return self.g_m[combo[0]]

        if all(cell in (-1, -2) for cell in self.g_m):
            return 0  # Ничья

        return None
    

    def end_game_message(self) -> bool:
        ans: str = input("do you wanna play again? (y/n):").strip()
        return True if ans.lower() == 'y' else False 


    def __reset_game_map(self) -> None:
        '''Очистка игровой карты'''
        
        self.__clear_console()
        self.g_m: List[int] = [
            1,2,3,
            4,5,6,
            7,8,9
        ]
        self.show_map()


    def start(self) -> Tuple[int, int]:
        self.show_map()
        while True:
            self.user_step()
            winner = self.who_winner()

            if winner == -1:
                print("YOU LOSE")
                self.losses += 1
                if self.end_game_message():
                    self.__reset_game_map()
                    continue
                return (self.wins, self.losses)
            elif winner == -2:
                print("YOU WON")
                self.wins += 1
                if self.end_game_message():
                    self.__reset_game_map()
                    continue
                return (self.wins, self.losses)
            elif winner == 0:
                print("DRAW")
                if self.end_game_message():
                    self.__reset_game_map()
                return (self.wins, self.losses)

            self.bot_step()
            winner = self.who_winner()

            if winner == -1:
                print("YOU LOSE")
                self.losses += 1
                if self.end_game_message():
                    self.__reset_game_map()
                    continue
                return (self.wins, self.losses)
            elif winner == -2:
                print("YOU WON")
                self.wins += 1
                if self.end_game_message():
                    self.__reset_game_map()
                return (self.wins, self.losses)
            elif winner == 0:
                print("DRAW")
                if self.end_game_message():
                    self.__reset_game_map()
                    continue
                return (self.wins, self.losses)
