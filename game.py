#coding=utf8

# Файл: game.py
# Содержит описание функций 
# контроля игрового процесса и вызова отрисовки 

# Подключение модуля графики
import view
# Подключение модуля поведения змейки
import snake

# Пуск игры
def play_game():    
    # Инициализация змейки
    player_snake = snake.Snake()
    
    # Инициализация отрисовщика
    viewer = view.Display(player_snake)
    # Передача отрисованного в Model (Snake)
    player_snake.set_borders(*viewer.get_borders())
    
    # Установка начального положения
    player_snake.restart()
    
    
    # Клавиши управления
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_QUIT = 32; # Код клавиши "Пробел"
    
    # Клавиши изменения направления
    KEY_UP    = ord('w');
    KEY_LEFT  = ord('a'); 
    KEY_DOWN  = ord('s') 
    KEY_RIGHT = ord('d')
    
    key = 0 # Переменная введенной клавиши  
    
    while key != KEY_QUIT: # Не нажата клавиша выхода 
        
        # Нажата клавиша перезапуска
        if(key == KEY_RESTART):
            player_snake.restart()
            
        # Изменяется направление змейки
        if(key == KEY_LEFT):
            player_snake.change_direction(player_snake.Direction.LEFT)
        elif(key == KEY_RIGHT):
            player_snake.change_direction(player_snake.Direction.RIGHT)
        elif(key == KEY_UP):
            player_snake.change_direction(player_snake.Direction.UP)
        elif(key == KEY_DOWN):
            player_snake.change_direction(player_snake.Direction.DOWN)
        
        # Возврат объекта window для управления после отрисовки
        screen = viewer.draw_game(player_snake) # Отрисовка кадра
        # Получение размера отрисованного поля змейкой
        player_snake.set_borders(*viewer.get_borders())
        
        key = screen.getch()  # Ожидание нажатия клавиши
        
    viewer.clear_game() # Стирает все игровые настройки

# Запуск игры
def main():
    play_game() 

if __name__ == "__main__":
    main()
