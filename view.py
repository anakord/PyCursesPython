#coding=utf8

# Файл: view.py
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

# Отрисовка надписей
# points - количество очков
# Возвращает количетво строк, которые занимает информация снизу
#   Указывается вручную
def draw_info(stdscr, points):
    height, width = stdscr.getmaxyx()
    
    stdscr.attron(curses.color_pair(1)) # Режим вывода текста
    
    # Вывод количества очков
    str_point = u"Очки " + str(points)
    stdscr.addstr(0, width-len(str_point), # Вывод справа 
                  str_point.encode('utf-8'));
    
    # Вывод подсказкок внизу экрана
    stdscr.addstr(height-3, 0, "P - пауза") 
    stdscr.addstr(height-2, 0, "R - перезапуск") 
    stdscr.addstr(height-1, 0, "Для выхода нажмите <SPACE>")    
    
    stdscr.attroff(curses.color_pair(1))
    
    # Возврат количества занятых строк снизу
    return 3
    
    
# Функция вывода ошибки на случай, если терминал сильно сжат
def draw_error(stdscr):
    # Строка ошибки
    STR_ERR = u"Увеличьте окно терминала!"
	
	# Расчет позиции для отображения по-середине
    height, width = stdscr.getmaxyx()
    pos_x = width // 2 - (len(STR_ERR) // 2) 
    pos_y = height // 2
    
    stdscr.attron(curses.color_pair(2)) 
    stdscr.attron(curses.A_BOLD) 
    
    stdscr.addstr(pos_y, pos_x, STR_ERR.encode('utf-8'))
    
    stdscr.attroff(curses.A_BOLD) 
    stdscr.attroff(curses.color_pair(2))  
	              
# Основная функция отрисовки (экран stdscr)
def draw_game(stdscr):
    
    curses.curs_set(False) # Сокрытие курсора
    
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
        draw_error(stdscr)
    else:	   
        
        #Отрисовка информационных надписей
        bottom_indent = draw_info(stdscr, 724)
        #Отрисовка границы
        border(stdscr, 0, 1, 
               width-1, height - (bottom_indent+1))

    stdscr.refresh()  # Обновление изменений



