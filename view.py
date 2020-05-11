#coding=utf8

# Файл: view.py
# Содержит описание функций вывода игрового поля на консоль
# с использованием библиотеки curses

# Использование Unicode для русского вывода
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

import curses # Библиотека для псевдографики

# Класс: Display
# Содержит поля и методы для отображения игры
# Методы:
#  draw_game: кадровая отрисовка всей игры
#   _draw_error: отрисовка окна ошибки
#   _draw_info: отрисовка информационных надписей
#   _draw_border: отрисовка границы
#  clear_game: стирает игровое поле и возращает к настройкам ОС
class Display(object):
     
    # Константы минимального размера консоли
    MIN_X = 44; MIN_Y = 8 
    
    # Поле экрана для методов отрисовки
    screen = curses.initscr()
    
    # Текущие размеры экрана
    height, width = screen.getmaxyx()
    
    def __init__(self):
        # Настройка ввода
        curses.curs_set(False) # Сокрытие курсора
        self.screen.keypad(True)
        curses.noecho() # Отключение ввода
        curses.cbreak()
        
        # Создание цветовых пар шрифт-фон
        curses.start_color()
        # Обычные надписи
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        
        #Первонача
        
    # Функция вывода ошибки на случай, если терминал сильно сжат
    def _draw_error(self):
        # Строка ошибки
        STR_ERR = u"Увеличьте окно терминала!"
        
        # Расчет позиции для отображения по-середине
        pos_x = self.width // 2 - (len(STR_ERR) // 2) 
        pos_y = self.height // 2
        
        self.screen.attron(curses.color_pair(2)) 
        self.screen.attron(curses.A_BOLD) 
        
        self.screen.addstr(pos_y, pos_x, STR_ERR.encode('utf-8'))
        
        self.screen.attroff(curses.A_BOLD) 
        self.screen.attroff(curses.color_pair(2))  

    # Отрисовка надписей
    # points - количество очков
    # Возвращает количетво строк, которые занимает информация снизу
    #   Указывается вручную
    def _draw_info(self, points):
        
        self.screen.attron(curses.color_pair(1)) # Режим вывода текста
        
        # Вывод количества очков
        str_point = u"Очки " + str(points)
        self.screen.addstr(0, self.width-len(str_point), # Вывод справа 
                      str_point.encode('utf-8'));
        
        # Вывод подсказкок внизу экрана
        self.screen.addstr(self.height-3, 0, "P - пауза") 
        self.screen.addstr(self.height-2, 0, "R - перезапуск") 
        self.screen.addstr(self.height-1, 0, "Для выхода нажмите <SPACE>")    
        
        self.screen.attroff(curses.color_pair(1))
        
        # Возврат количества занятых строк снизу
        return 3
        
    # Функция отрисовки границы игрового поля 
    # std-решение border не поддерживает пользовательского расположения 
    # x1, y1 - координаты первой вершины границы 
    # x2, y2 - координаты второй вершины границы 
    ## Реализовать как перегрузку метода
    def _draw_border(self, x1, y1, x2, y2):
        # Константы символов границы
        CH_TLCORNER = '╔'; CH_TRCORNER = '╗' 
        CH_HORLINE = '═'; CH_VERTLINE = '║'
        CH_BLCORNER = '╚'; CH_BRCORNER = '╝'
        
        # Отрисовка углов
        self.screen.addstr(y1,x1, CH_TLCORNER)
        self.screen.addstr(y2, x1, CH_BLCORNER)
        self.screen.addstr(y1, x2, CH_TRCORNER)
        self.screen.addstr(y2, x2, CH_BRCORNER)
        
        # Отрисовка самой границы
        for x in range(x1+1, x2): # Горизонтальные линии
            self.screen.addstr(y1,x, CH_HORLINE)
            self.screen.addstr(y2,x, CH_HORLINE)
        for y in range(y1+1, y2): # Вертикальные линии
            self.screen.addstr(y,x1, CH_VERTLINE)
            self.screen.addstr(y,x2, CH_VERTLINE)
    
    # Функция определения изменения размера экрана
    ## Пока не используется
    def _is_resized(self):
        buf_y, buf_x = self.screen.getmaxyx()
        return self.width != buf_x and self.height != buf_y

    # Основная функция отрисовки 
    def draw_game(self):
        
        # Обновление размерности поля
        self.height, self.width = self.screen.getmaxyx()
        
        # Очищение, обновление экрана  
        self.screen.clear()
        self.screen.refresh()
        
        # Проверка на достаточный размер окна для игры
        if self.width < Display.MIN_X or self.height < Display.MIN_Y:
            self._draw_error()
        else:	        
            #Отрисовка информационных надписей
            bottom_indent = self._draw_info(724)
            #Отрисовка границы
            self._draw_border(0, 1, 
                   self.width-1, self.height - (bottom_indent+1))

        self.screen.refresh()  # Обновление изменений
        
        # Возврат отрисованного экрана
        return self.screen 
        
    # Функция стирания интерфейса и возвращения в cmd
    def clear_game(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()



