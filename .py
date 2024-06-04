
import pygame
import random
import copy

# 파이 게임 초기화
pygame.init() 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 크기 설정
clock = pygame.time.Clock() 

# 게임에 필요한 변수 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
large_font = pygame.font.SysFont('malgungothic', 72)  # 폰트 
small_font = pygame.font.SysFont('malgungothic', 36)
score = 0
high_score = 0
game_over = False 
start_font = pygame.font.SysFont('malgungothic', 32)
start_text = start_font.render('스페이스바를 눌러 게임을 시작해주세요', True, YELLOW)
description_font = pygame.font.SysFont('malgungothic', 28)

# 최고 점수를 파일에서 불러오기
def load_high_score():
    global high_score
    with open('high_score.txt', 'r') as file:
            high_score = int(file.read())

# 최고 점수를 파일에 저장하기
def save_high_score():
    global high_score
    with open('high_score.txt', 'w') as file:
        file.write(str(high_score))

#게임 재시작
def restart_game():
    global game_over, score, airplane, obstacle, airplane_dy
    game_over = False
    score = 0
    airplane = airplane_image.get_rect(centery=SCREEN_HEIGHT // 2)
    airplane_dy = 0  # 비행기 속도 초기화
    obstacle.topleft = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - obstacle_image.get_height()))
load_high_score()

airplane_image = pygame.image.load('airplane.png')  # 비행기 이미지 
airplane = airplane_image.get_rect(centery=SCREEN_HEIGHT // 2)  # 화면 
airplane_dy = 2  

explosion_image = pygame.image.load("explosion.png")  # 충돌 이미지 

obstacle_image = pygame.image.load('bomb.png')
obstacle = obstacle_image.get_rect(topleft=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - obstacle_image.get_height()))) # 랜덤 위치 

#충돌 여부 
def detect_collision(airplane, obstacle): 
    return airplane.colliderect(obstacle)

rects = []  
for column_index in range(1200): 
    rect = pygame.Rect(column_index * 10, 100, 10, 400)  
    rects.append(rect)  
slope = 2

pygame.mixer.init()  # 초기
pygame.mixer.music.load('music.mid')  # 배경 음악
pygame.mixer.music.play(-1)  # -1: 무한 반복, 0: 한번
explosion_sound = pygame.mixer.Sound('explosion.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
game_started = False

while True: 
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True
            if event.key == pygame.K_UP:
                airplane_dy = -5
            elif event.key == pygame.K_DOWN:
                airplane_dy = 5
            elif event.key == pygame.K_SPACE and game_over:  
                restart_game()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                airplane_dy = 0 #고정  

    if game_started and not game_over:  # 게임이 시작되었고 종료 상태가 아닐 때만 실행
        airplane.centery += airplane_dy
        new_rect = copy.deepcopy(rects[-1])
        test_rect = copy.deepcopy(rects[-1])
        test_rect.top = test_rect.top + slope # 사각형 수직 방향 이동 
        if test_rect.top <= 0 or test_rect.bottom >= SCREEN_HEIGHT:
            slope = random.randint(2, 6) * (-1 if slope > 0 else 1)  # 반대 방향으로 기울어지게 하기
        new_rect.left = new_rect.left + 10 
        new_rect.top = new_rect.top + slope # 사각형 위 아래 움직이기 
        rects.append(new_rect)
        for rect in rects:
            rect.left = rect.left - 10
        del rects[0]

        if airplane.top < rects[0].top or airplane.bottom > rects[0].bottom: #사각형 상단보다 위에 있거나 아래 있는지 확인 
            game_over = True
        
        for rect in rects:
            pygame.draw.rect(screen, BLACK, rect)

        obstacle.left -= 25
        if obstacle.right < 0:
            obstacle.topleft = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - obstacle_image.get_height())) # 오른쪽 배치 
            score += 1

        # 장애물 그리기
        screen.blit(obstacle_image, obstacle)

        # 충돌 감지
        if detect_collision(airplane, obstacle):
            game_over = True
            explosion_sound.play()
        
        # 게임 오버 처리
        if game_over:
            game_over_sound.play()
            if score > high_score:
                high_score = score
                save_high_score()
            
            screen.blit(explosion_image, (obstacle.left, obstacle.top))
            
    else:
        screen.blit(start_text, start_text.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
    
    # 화면 업데이트
    screen.blit(airplane_image, airplane)

    score_image = small_font.render('점수: {}'.format(score), True, YELLOW)
    screen.blit(score_image, (10, 10))

    high_score_image = small_font.render('최고 점수: {}'.format(high_score), True, YELLOW)
    screen.blit(high_score_image, (10, 50))

    pygame.display.update() 
    clock.tick(40)

