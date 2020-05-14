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
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_QUIT = 32; # Код клавиши "Пробел"
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
    
    key = KEY_RIGHT # Переменная введенной клавиши  

    # Функция возвращает, нажата ли клавиша выхода
    def _is_quit(self):
        return self.key == Controller.KEY_QUIT
    
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
            
            self.screen.timeout(200) # Задержка экрана
            
            self.key = self.screen.getch()
            
            # Нажата клавиша рестарта
            if self._is_restart():
                self.player_snake.restart()
            
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
