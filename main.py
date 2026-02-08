import random # випадкові числа
import pygame # гра
import sys # системні функції
import os # системні функції

pygame.init() # ініціалізація
screen = pygame.display.set_mode((500, 500)) # розмір

clock = pygame.time.Clock() # час
fps = 60 # кадри

def main_menu():
    font = pygame.font.SysFont("Comic Sans MS", 30)
    title = font.render("GAME SNAKE", True, (0, 255, 0))
    play_text = font.render("Press any key to Play", True, (255, 255, 255))
    
    while True:
        screen.fill((0, 0, 0))#
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 150))
        screen.blit(play_text, (screen.get_width() // 2 - play_text.get_width() // 2, 300))
        
        pygame.display.update()
        
        for event in pygame.event.get(): # події
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        clock.tick(fps) 
# меню закінчення гри
def game_over_screen(score): 
    font_big = pygame.font.SysFont("Comic Sans MS", 50)
    font_small = pygame.font.SysFont("Comic Sans MS", 30)
    
    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 150))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 250))
        screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 350))
        
        pygame.display.update()
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    os.execv(sys.executable, ['python'] + sys.argv)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(fps)

NEON_COLORS = [ (255, 20, 147), # neon pink
                (57, 255, 20), # neon green
                (0, 255, 255), # cyan
                (255, 255, 0), # yellow
                (255, 105, 180), # hot pink
                (0, 191, 255), # deep sky blue
                (255, 0, 255), # magenta
                (0, 255, 127), # spring green
                (204, 0, 255), # purple 
                (255, 165, 0) # orange
] 

def generate_apple(snake): # генерація яблука
    total_cells = screen.get_width() // circle_size * screen.get_height() // circle_size 
    if len(snake) >= total_cells: 
        return None # немає місця то перемога

    while True:
        apple_x = random.randint(1, screen.get_width() // circle_size -2) * circle_size # випадкове місце
        apple_y = random.randint(1, screen.get_height() // circle_size -2) * circle_size
        
        # перевірка щоб яблуко не заходило на область score
        if apple_x < 100 and apple_y < 40:
            continue
            
        if (apple_x, apple_y) not in snake:
            apple_color = random.choice(NEON_COLORS)
            return apple_x, apple_y, apple_color

speed = 10
frame_count = 0
circle_size = 15
main_menu()
pygame.event.clear()
score = 0
font = pygame.font.SysFont("Comic Sans MS", 25)


x = (screen.get_width() // 2 // circle_size) * circle_size # початкова позиція
y = (screen.get_height() // 2 // circle_size) * circle_size

center = x + circle_size // 2, y + circle_size //2 # центр
radius_big= circle_size // 2 
radius_small = circle_size // 3 
snake = [
    (x + circle_size * 2, y),  # голова справа
    (x + circle_size, y),       # тіло
    (x, y)                      # хвіст зліва
]
apple_x, apple_y, apple_color = generate_apple(snake) # генерація яблука
apple_center = apple_x + circle_size // 2, apple_y + circle_size //2 # центр яблука

dx = circle_size
dy = 0


while True: # основний цикл

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -circle_size
            if event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = circle_size
            if event.key == pygame.K_LEFT and dx == 0:
                dx = -circle_size
                dy = 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx = circle_size
                dy = 0     

            #wasd
            elif event.key == pygame.K_w and dy == 0:
                dx = 0
                dy = -circle_size
            elif event.key == pygame.K_s and dy == 0:
                dx = 0
                dy = circle_size
            elif event.key == pygame.K_a and dx == 0:
                dx = -circle_size
                dy = 0
            elif event.key == pygame.K_d and dx == 0:
                dx = circle_size
                dy = 0  
              
    frame_count += 1 # лічильник кадрів
    if frame_count % speed == 0:
        frame_count = 0
        
        new_head = (snake[0][0] + dx, snake[0][1] + dy)# нова позиція голови


        if 0 <= new_head[0] < screen.get_width() and 0 <= new_head[1] < screen.get_height(): # перевірка на вихід за межі екрану
            snake.insert(0, new_head)
        
            if new_head[0] == apple_x and new_head[1] == apple_y: 
                score += 10
                # з’їла яблуко не видаляємо хвіст
                result = generate_apple(snake)  
                if result is None:
                    # перемога
                    screen.fill((0, 0, 0))
                    font_win = pygame.font.SysFont("Comic Sans MS", 50)
                    win_text = font_win.render("WIN", True, (0, 255, 0))
                    screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, 
                                           screen.get_height() // 2 - win_text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.wait(4000)
                    exit()
                else:
                    apple_x, apple_y, apple_color = result 
            else:
                snake.pop()      
        # самопоїдання    
            if new_head in snake[1:]:
                indx = snake.index(new_head, 1)  # знаходимо індекс зіткнення
                snake = snake[:indx + 1]  # залишаємо лише частину до зіткнення
                           
        else:
            game_over_screen(score)
            exit()

    screen.fill((0, 0, 0)) 
    
    for i, (body_x, body_y) in enumerate(snake): 
        center = body_x + circle_size // 2, body_y + circle_size //2
        if i == 0: # голова
            pygame.draw.circle( 
                screen,
                (0, 200, 0), #color
                center,
                radius_big
            )
            pygame.draw.circle(
                screen,
                (0, 100, 0), 
                center,
                radius_small
            )
            # очі
            eye_radius = 3
            eye_offset_x = 4
            eye_offset_y = 6

            if dx > 0: # вправо
                left_eye = (center[0] + eye_offset_x, center[1] - eye_offset_y)
                right_eye = (center[0] + eye_offset_x, center[1] + eye_offset_y)
            elif dx < 0: # вліво
                left_eye = (center[0] - eye_offset_x, center[1] - eye_offset_y)
                right_eye = (center[0] - eye_offset_x, center[1] + eye_offset_y)
            elif dy > 0: # вниз
                left_eye = (center[0] - eye_offset_x, center[1] + eye_offset_y)
                right_eye = (center[0] + eye_offset_x, center[1] + eye_offset_y)
            elif dy < 0: # вгору
                left_eye = (center[0] - eye_offset_x, center[1] - eye_offset_y)
                right_eye = (center[0] + eye_offset_x, center[1] - eye_offset_y)
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                left_eye,
                eye_radius
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                right_eye,
                eye_radius
            )
            # зіниці
            pygame.draw.circle(
                screen,
                (0, 0, 0),
                left_eye, 1
            )
            pygame.draw.circle(
                screen,
                (0, 0, 0),
                right_eye, 1
            )
        else: # тіло
            pygame.draw.circle(
                screen,
                (0, 200, 0), #color
                center,
                radius_big
            )
            pygame.draw.circle(
                screen,
                (0, 100, 0), 
                center,
                radius_small
            )
    apple_center = apple_x + circle_size // 2, apple_y + circle_size //2 # центр яблука
    
    #яблуко
    pygame.draw.circle(
        screen,
        apple_color, 
        apple_center,
        radius_big
    )
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()
    clock.tick(fps)




