#coding=utf8

# Файл: draw.py
# Содержит описание функций вывода игрового поля на консоль
# с использованием библиотеки curses

import curses # Библиотека для псевдографики

# Использование Unicode для русского вывода
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# Основная функция отрисовки (экран stdscr)
def draw_game(stdscr):
    
    # Константы размера консоли в символах 
    WIDTH = 80; HEIGHT = 24
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_QUIT = 32; # Код клавиши "Пробел"
    
    key = 0 # Переменная введенной клавиши
    
    # Очищение и обновление экрана  
    stdscr.clear()
    stdscr.refresh()
    
    # Создание цветовых пар шрифт-фон
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    # Вывод подсказки для выхода внизу экрана
    
    stdscr.addstr(HEIGHT-1, 0, "Перезапуск - R, Для выхода нажмите <SPACE>", 
                  curses.color_pair(1))
                  
    while (key != KEY_QUIT): # Не нажата клавиша выхода
     
        #Запрет на изменение размера окна
        while True:
            if(HEIGHT, WIDTH != stdscr.getmaxyx()):
               stdscr.resize(HEIGHT, WIDTH)
        #stdscr.refresh()  # Обновление изменений
        
        key = stdscr.getch()  # Ожидание нажатия клавиши

# Запуск отрисовки игры
def main():
    # Запрет на изменение размера окна
    
    curses.wrapper(draw_game)

if __name__ == "__main__":
    main()

