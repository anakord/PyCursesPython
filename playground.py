#coding=utf8

# Файл: draw.py
# Содержит описание функций вывода игрового поля на консоль
# с использованием библиотеки curses

import curses # Библиотека для псевдографики

# Использование Unicode для русского вывода
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
 
# Функция отрисовки границы игрового поля 
# std-решение border не поддерживает пользовательского расположения 
# x1, y1 - координаты первой вершины границы 
# x2, y2 - координаты второй вершины границы 
## Реализовать как перегрузку метода
def border(self, x1, y1, x2, y2):
    # Константы символов границы
    CH_TLCORNER = '╔'; CH_TRCORNER = '╗' 
    CH_HORLINE = '═'; CH_VERTLINE = '║'
    CH_BLCORNER = '╚'; CH_BRCORNER = '╝'
    
    # Отрисовка углов
    self.addstr(y1,x1, CH_TLCORNER)
    self.addstr(y2, x1, CH_BLCORNER)
    self.addstr(y1, x2, CH_TRCORNER)
    self.addstr(y2, x2, CH_BRCORNER)
    
    # Отрисовка самой границы
    for x in range(x1+1, x2): # Горизонтальные линии
        self.addstr(y1,x, CH_HORLINE)
        self.addstr(y2,x, CH_HORLINE)
    for y in range(y1+1, y2): # Вертикальные линии
        self.addstr(y,x1, CH_VERTLINE)
        self.addstr(y,x2, CH_VERTLINE)
               
# Основная функция отрисовки (экран stdscr)
def draw_game(stdscr):
    # Константы минимального размера консоли
    MIN_X = 44; MIN_Y = 10 
    # Переменные размера консоли в символах 
    width = 80; height = 24 # Стандартный размер
    # Обновление размерности поля
    height, width = stdscr.getmaxyx()
    
    # Создание цветовых пар шрифт-фон
    curses.start_color()
    # Обычные надписи
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    # Очищение, обновление экрана  
    stdscr.clear()
    stdscr.refresh()
    
    # Проверка на достаточный размер окна для игры
    if width < MIN_X or height < MIN_Y:
        # Вывод информации об этом
        stdscr.attron(curses.color_pair(2)) 
        stdscr.attron(curses.A_BOLD) 
        stdscr.addstr(1, 1, "Увеличьте окно терминала!")
        stdscr.refresh()
        stdscr.attroff(curses.A_BOLD) 
        stdscr.attroff(curses.color_pair(2))        
    
    else:
		   
        #Отрисовка границы
        border(stdscr, 0, 1, width-1, height-4)
       
        stdscr.attron(curses.color_pair(1)) # Режим вывода текста
        # Вывод количества очков
        str_point = u"Очки 9999"
        stdscr.addstr(0, width-len(str_point), #вывести по правую сторону 
                      str_point.encode('utf-8'));
        # Вывод подсказкок внизу экрана
        stdscr.addstr(height-3, 0, "P - пауза") 
        stdscr.addstr(height-2, 0, "R - перезапуск") 
        stdscr.addstr(height-1, 0, "Для выхода нажмите <SPACE>")    

        stdscr.refresh()  # Обновление изменений

# Пуск игры
def play_game(stdscr):
    
    curses.curs_set(False) # Сокрытие курсора
        
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_QUIT = 32; # Код клавиши "Пробел"
    
    key = 0 # Переменная введенной клавиши  
                 
    while key != KEY_QUIT: # Не нажата клавиша выхода 
        
        draw_game(stdscr) # Отрисовка поля и надписей
        
        key = stdscr.getch()  # Ожидание нажатия клавиши


# Запуск игры
def main():
    curses.wrapper(play_game)

if __name__ == "__main__":
    main()

