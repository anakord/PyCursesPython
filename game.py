#coding=utf8

# Файл: game.py
# Содержит описание класса Controller
# контролирующего игровой процесс и вызов отрисовки 

# Подключение модуля графики
import view
# Подключение модуля поведения змейки
import snake

class Controller():
    
    # Клавиши управления
    KEY_QUIT = 32; # Код клавиши "Пробел"
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_PAUSE = ord('p')
    # Клавиши изменения направления
    KEY_UP    = ord('w')
    KEY_LEFT  = ord('a') 
    KEY_DOWN  = ord('s') 
    KEY_RIGHT = ord('d')

    # Инициализация змейки
    player_snake = snake.Snake()
    # Инициализация отрисовщика
    viewer = view.Display(player_snake)
    # Установка начального положения
    player_snake.restart()
    # Первая отрисовка
    screen = viewer.draw_game(player_snake)
    # Модификатор паузы
    PAUSE_MODE = False
       
    key = KEY_RIGHT # Переменная исполняемой клавиши
    # Переменная введенной клавиши
    # Для предотвращения излишнего обновления экрана
    buffer_key = key  
    
    # Стартовая скорость
    START_SPEED = 1000
    # Размерность, при которой происходит увеличение скорости
    INCREASING_SIZE = 5
 
    # Модификатор скорости
    speed_modif = 1
    
    # Функция возвращает необходимую скорость в милисекундах
    def speed(self):
        speed_modif \
          = self.player_snake.get_size() // self.INCREASING_SIZE + 1 
        return self.START_SPEED // speed_modif
    
    # Функция возвращает, нажата ли клавиша выхода
    def _is_quit(self):
        return self.key == Controller.KEY_QUIT
    
    # Функция постановки на паузу
    def _is_pause(self):
        if self.key == Controller.KEY_PAUSE:
            self.PAUSE_MODE = not self.PAUSE_MODE
        return self.PAUSE_MODE
    
    # Функция возвращает, нажат ли перезапуск
    def _is_restart(self):
        return self.key == Controller.KEY_RESTART
        
    # Функция изменяет направление змейки
    def _set_direction(self):
        if self.key == Controller.KEY_LEFT: self.player_snake. \
           change_direction(self.player_snake.Direction.LEFT)
        elif self.key == Controller.KEY_RIGHT: self.player_snake. \
           change_direction(self.player_snake.Direction.RIGHT)
        elif self.key == Controller.KEY_UP: self.player_snake. \
           change_direction(self.player_snake.Direction.UP)
        elif self.key == Controller.KEY_DOWN: self.player_snake. \
           change_direction(self.player_snake.Direction.DOWN)
        
    # Пуск игры
    def play_game(self):    
        
        # Пока не будет введена клавиша выхода
        while not self._is_quit():
            
            # Задержка экрана
            self.screen.timeout(self.speed()) 
            
            self.key = self.screen.getch()
            
            # Нажата клавиша рестарта
            if self._is_restart():
                self.player_snake.restart()
            
            if not self._is_pause():
                
                # Если змейка наткнулась на еду
                if self.player_snake.is_eaten():
                    # Она ее съедает
                    self.player_snake.eat() 
                    # Респавнится новая еда
                    self.player_snake.food_spawn() 
                        
                if not self.player_snake.is_gameover():
                    # Изменяется направление змейки
                    self._set_direction()
                    # Змейка делает шаг
                    self.player_snake.make_step()
                    
            # Отрисовка кадра    
            self.viewer.draw_game(self.player_snake) 
                
        # Стирает все игровые настройки
        self.viewer.clear_game() 

# Запуск игры
def main():
    game = Controller()
    game.play_game() 

if __name__ == "__main__":
    main()
