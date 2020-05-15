#coding=utf8

# Файл: view.py
# Содержит описание функций вывода игрового поля на консоль
# Реализация функций в классе Display
# с использованием библиотеки curses

# Использование Unicode для русского вывода
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

import curses # Библиотека для псевдографики
import snake # Библиотека для определения положения змейки

# Класс: Display
# Содержит поля и методы для отображения игры
# Методы:
#  draw_game: кадровая отрисовка всей игры
#   _draw_error: отрисовка окна ошибки
#   _draw_info: отрисовка информационных надписей
#   _draw_border: отрисовка границы
#   _draw_snake(snake): отрисовывает полученную змейку
#  clear_game: стирает игровое поле и возращает к настройкам ОС
class Display():
     
    # Константы минимального размера консоли
    MIN_X = 44; MIN_Y = 8 
    
    # Константы отступов при отрисовке границ игрового поля
    LEFT_INDENT_X = 0; RIGHT_INDENT_X = 1
    UP_INDENT_Y   = 1; DOWN_INDENT_Y = 4
    
    # Поле экрана для методов отрисовки
    screen = curses.initscr()
    # Текущие размеры экрана
    height, width = screen.getmaxyx()
    
    def __init__(self, st_snake):
        
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
        
        # Обновление размерности поля
        self.height, self.width = self.screen.getmaxyx()
        # Получение размера отрисованного поля змейкой
        st_snake.set_borders(*self.get_borders())
        
    # Функция вывода ошибки на случай, если терминал сильно сжат
    def _draw_error(self):
        
        self.screen.erase()
        
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
        str_point = u"Очки: " + str(points) # Голова не учитывается 
        self.screen.addstr(0, self.width-len(str_point), # Вывод справа 
                      str_point.encode('utf-8'));
        
        # Вывод подсказкок внизу экрана
        self.screen.addstr(self.height-3, 0, "WASD - управление; P - пауза") 
        self.screen.addstr(self.height-2, 0, "R - перезапуск") 
        self.screen.addstr(self.height-1, 0, "Для выхода нажмите <SPACE>")    
        
        self.screen.attroff(curses.color_pair(1))
        
    # Функция отрисовки границы игрового поля 
    # std-решение border не поддерживает пользовательского расположения 
    # x1, y1 - координаты первой вершины границы 
    # x2, y2 - координаты второй вершины границы 
    ## Реализовать как перегрузку метода
    def _draw_border(self):
        # Константы символов границы
        CH_TLCORNER = '╔'; CH_TRCORNER = '╗' 
        CH_HORLINE = '═'; CH_VERTLINE = '║'
        CH_BLCORNER = '╚'; CH_BRCORNER = '╝'
        
        # Получение координат отрисовки границ 
        x1 = self.LEFT_INDENT_X; 
        y1 = self.UP_INDENT_Y     
        x2 = self.width - self.RIGHT_INDENT_X
        y2 = self.height - self.DOWN_INDENT_Y
        
        # Отрисовка углов
        self.screen.addch(y1,x1, CH_TLCORNER)
        self.screen.addch(y2, x1, CH_BLCORNER)
        self.screen.addch(y1, x2, CH_TRCORNER)
        self.screen.addch(y2, x2, CH_BRCORNER)
        
        # Отрисовка самой границы
        for x in range(x1+1, x2): # Горизонтальные линии
            self.screen.addch(y1,x, CH_HORLINE)
            self.screen.addch(y2,x, CH_HORLINE)
        for y in range(y1+1, y2): # Вертикальные линии
            self.screen.addch(y,x1, CH_VERTLINE)
            self.screen.addch(y,x2, CH_VERTLINE)
        
        # Изменение объекта st_snake из модуля графики ?!
        # Установка нового размера змейки
    
    # Функция отрисовки еды
    # st_snake - текущее состояние (status) змейки
    def _draw_food(self, st_snake):
		
        CH_FOOD = '*'
        
        food = tuple(st_snake.get_food_pos())
        for [pos_x, pos_y] in food:
            self.screen.addch(pos_y + self.UP_INDENT_Y,   
                              pos_x + self.LEFT_INDENT_X, CH_FOOD)
		
    # Функция отрисовки змейки
    # st_snake - текущее состояние (status) змейки
    def _draw_snake(self, st_snake):
        # Символы изображения головы змейки
        # в зависимости от направления движения
        СH_HEAD_LEFT = "ᐊ"; СH_HEAD_RIGHT = "ᐅ"
        CH_HEAD_UP = "ᐃ"; СH_HEAD_DOWN = "ᐁ"
        CH_HEAD_DEAD = "✠"
        # Символ изображения тела
        CH_BODY = "#" 
        
        CH_HEAD = СH_HEAD_RIGHT
        
        # Отрисовка тела
        body = tuple(st_snake.get_body())
        for [pos_x, pos_y] in body: # Проход всех пар XY
            # Получение координат головы
            self.screen.addch(pos_y + self.UP_INDENT_Y,   
                               pos_x + self.LEFT_INDENT_X, CH_BODY)
                               
        # Отрисовка головы
        # Перевод координат змейки в координаты поля
        # Отступ границы слева
        pos_x = st_snake.get_headX() + self.LEFT_INDENT_X 
        # Отступ надписи "Очки ..." + граница сверху
        pos_y = st_snake.get_headY() + self.UP_INDENT_Y 
        # Уточнение текущего направления головы
        cur_direction = st_snake.get_direction()
        if cur_direction == st_snake.Direction.LEFT: 
            CH_HEAD = СH_HEAD_LEFT
        elif cur_direction == st_snake.Direction.RIGHT: 
            CH_HEAD = СH_HEAD_RIGHT
        elif cur_direction == st_snake.Direction.UP: 
            CH_HEAD = CH_HEAD_UP
        elif cur_direction == st_snake.Direction.DOWN: 
            CH_HEAD = СH_HEAD_DOWN
        # Если проигрыш - нарисовать мертвую голову
        if st_snake.is_gameover():
            CH_HEAD = CH_HEAD_DEAD
        self.screen.addch(pos_y, pos_x, CH_HEAD)        
        
    # Функция вычисления размеров игрового поля
    def get_borders(self):
        borderX = self.width                  \
          - (self.LEFT_INDENT_X + self.RIGHT_INDENT_X)
        borderY = self.height                 \
          - (self.UP_INDENT_Y + self.DOWN_INDENT_Y)
        return borderX, borderY 
               
    
    # Основная функция отрисовки 
    # snake - текущий снимок состояния змейки для отрисовки
    def draw_game(self, st_snake):
        
        # Обновление размерности поля
        self.height, self.width = self.screen.getmaxyx()
        # Получение размера отрисованного поля змейкой
        st_snake.set_borders(*self.get_borders())
        
        # Очищение экрана  
        self.screen.erase()
  
        # Проверка на достаточный размер окна для игры
        if self.width < Display.MIN_X or self.height < Display.MIN_Y:
            self._draw_error()
        else:	        
            # Если консоль стала меньше, чем нужно
            try:
                # Отрисовка информационных надписей
                self._draw_info(st_snake.get_size())
                # Отрисовка границы
                self._draw_border()
                # Отрисовка еды
                self._draw_food(st_snake)
                # Отрисовка змейки
                self._draw_snake(st_snake)
            except: self._draw_error()
            
            self.screen.refresh()  # Обновление изменений
            
        # Возврат отрисованного экрана
        return self.screen 
        
    # Функция стирания интерфейса и возвращения в режим cmd
    def clear_game(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        




