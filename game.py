#coding=utf8

# Файл: game.py
# Содержит описание функций 
# контроля игрового процесса и вызова отрисовки 

# Подключение модуля графики
import view
# Подключения стартера режима curses
from curses import wrapper as starter

# Пуск игры
def play_game(stdscr):    
        
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_QUIT = 32; # Код клавиши "Пробел"
    
    key = 0 # Переменная введенной клавиши  
                 
    while key != KEY_QUIT: # Не нажата клавиша выхода 
        
        view.draw_game(stdscr) # Отрисовка поля и надписей
        
        key = stdscr.getch()  # Ожидание нажатия клавиши

# Запуск игры
def main():
    starter(play_game)

if __name__ == "__main__":
    main()
