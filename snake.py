#coding=utf8

# Файл: snake.py
# Содержит класс Snake, описывающий состояние и логику змейки

# Подключение именованных кортежей
from collections import namedtuple
import enum

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
        LEFT = _d_info(-1, 0)
        RIGHT = _d_info(+1, 0)
        UP = _d_info(0, +1) 
        DOWN = _d_info(0, -1)
    
    # Стартовое направление змейки
    _start_direction = Direction.RIGHT    
    
    # Текущее направление змейки
        
    # Размер змейки (изначально 1)
    _size = 1
    
    # Текущее положение головы змейки
    _headX = 0 
    _headY = 0
    
    # Границы игрового поля (по умолчанию)
    _borderX = 0 
    _borderY = 0
    
    # Функциии get_headX(), get_headY()
    # Получение текущего положения головы змейки по X и Y, соответственно
    def get_headX(self):
        return self._headX
    def get_headY(self):
        return self._headY

    # Функция получения размера змейки
    def get_size(self):
        return self._size
        
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
        self._cur_direction = direction
    
    # Функция 1 шага змейки
    def make_step(self):
        self.headX = self.headX + self._cur_direction.value.dx
        self.headY = self.headY + self._cur_direction.value.dy
        
    # Первоначальные настройки
    def restart(self):
        # Централизация головы змейки
        self._headX = self._borderX // 2
        self._headY = self._borderY // 2
        # Установка начального направления
        self._cur_direction = self._start_direction
        # Обнуление очков
        self._size = 1
