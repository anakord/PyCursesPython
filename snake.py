#coding=utf8

# Файл: snake.py
# Содержит класс Snake, описывающий состояние и логику змейки

# Подключение именованных кортежей и перечислений
from collections import namedtuple
import enum
# Подключение рандома
import random

# Класс: snake.py
# Описивает поведение змейки, коллизии с границами, телом и едой
# Direction - направления (вверх, вниз, влево, вправо)
# cur_direction - текущее направление 
# size - размер змейки

class Snake():
	
    # Перечисление направлений змейки с указанием изменения координат
    # dx - по X, dy - по Y
    class Direction(enum.Enum):
        # Информация о конкретном направлении
        _d_info = namedtuple('DiractionInfo', ['dx', 'dy']) 
		
        # Перечисление всех 4 направлений
        # Для координат от верхнего левого угла
        LEFT = _d_info(-1, 0)
        RIGHT = _d_info(+1, 0)
        UP = _d_info(0, -1) 
        DOWN = _d_info(0, +1)
    
    # Стартовое направление змейки
    _start_direction = Direction.RIGHT    
    
    # Координаты тела змейки в списке
    # Хранятся в виде [[x1,y1],[x2,y2],...]
    _body = []
    
    # Координаты расположения еды на поле
    # Хранятся в виде [[x1,y1],[x2,y2],...]
    _food = []
    
    # Границы игрового поля (по умолчанию)
    _borderX = 80; _borderY = 24
        
    # Текущее положение головы змейки
    _headX = 0; _headY = 0

    # Функциии get_headX(), get_headY()
    # Получение текущего положения головы змейки по X и Y, соответственно
    def get_headX(self):
        return self._headX
    def get_headY(self):
        return self._headY

    # Функция получения тела змейки в виде [x, y]
    def get_body(self):
        return self._body
    
    # Функция получения позиции еды
    def get_food_pos(self):
        return self._food
        
    # Функция получения размера змейки
    def get_size(self):
        return len(self._body)
        
    # Функция получения текущего направления движения
    def get_direction(self):
        return self._cur_direction
    
    # Функция установки размеров поля 
    # x, y - размеры поля
    def set_borders(self, x, y):
        self._borderX = x
        self._borderY = y
        
    # Функция изменения направления змейки
    def change_direction(self, direction):
        # Запрет на изменение движения на противоположное
        if self._cur_direction.value.dx != -direction.value.dx \
        and self._cur_direction.value.dy != direction.value.dy:
            self._cur_direction = direction
    
    # Функция 1 шага змейки
    def make_step(self):
        # Добавить тело на место продвинувшейся головы
        self._body.append([self._headX, self._headY])
        # Удалить единичный участок тела с конца
        del self._body[0]
        # Изменить положение головы
        self._headX = self._headX + self._cur_direction.value.dx
        self._headY = self._headY + self._cur_direction.value.dy
    
    # Функция спавна еды
    def food_spawn(self):
        random.seed()
        self._food.clear() # Убрать старую еду
        # Рандомизация места 
        # От начала поля минус 1 клетка границы
        spawnX = random.randint(1, self._borderX-1) 
        spawnY = random.randint(1, self._borderY-1)
        # Если рандомизация совпала с телом - повторить
        while [spawnX, spawnY] in self._body and \
              [spawnX, spawnY] in [self._headX, self._headY]:
            spawnX = random.randint(1, self._borderX)
            spawnY = random.randint(1, self._borderY)
        self._food.append([spawnX, spawnY])
        
    # Функция добавления тела при съедении
    def eat(self):
        self._body.append([self._headX - self._cur_direction.value.dx, 
                           self._headY - self._cur_direction.value.dy])
    
    # Функция возвращает, съела ли змейка фрукт
    def is_eaten(self):
        return [self._headX, self._headY] in self._food 
    
    # Функция проверки на проигрыш  
    # Возвращает:
    #  True - змейка врезалась
    #  False - все нормально  
    def is_gameover(self):
        # Проверка по границе и проверка по коллизии с телом
        return self._headX == 0 or self._headX == self._borderX \
            or self._headY == 0 or self._headY == self._borderY \
            or [self._headX, self._headY] in self._body  

        
    # Первоначальные настройки
    def restart(self):
        # Стирание тела и еды на поле
        self._body.clear()
        self._food.clear()
        # Централизация головы змейки
        self._headX = self._borderX // 2
        self._headY = self._borderY // 2
        # Установка начального направления
        self._cur_direction = self._start_direction
        
        # Респавн еды
        self.food_spawn()

        
