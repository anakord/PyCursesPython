#coding=utf8

# Файл: game.py
# Содержит описание функций 
# контроля игрового процесса и вызова отрисовки 

# Подключение модуля графики
import view

# Пуск игры
def play_game():    
    
    # Инициализация отрисовщика
    viewer = view.Display()
    
    KEY_RESTART = ord('r') # Код клавиши перезапуска
    KEY_QUIT = 32; # Код клавиши "Пробел"
    
    key = 0 # Переменная введенной клавиши  
                 
    while key != KEY_QUIT: # Не нажата клавиша выхода 
        
        screen = viewer.draw_game() # Отрисовка поля и надписей
        
        key = screen.getch()  # Ожидание нажатия клавиши
        
    viewer.clear_game() # Стирает все игровые настройки

# Запуск игры
def main():
    play_game() 

if __name__ == "__main__":
    main()
