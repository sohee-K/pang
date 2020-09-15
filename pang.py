import pygame
import os

pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Pang!")

# FPS
clock = pygame.time.Clock()

# 배경 불러오기
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "pang_images")
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 무대 불러오기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 0.5

# 무기 불러오기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

# 무기 발사 속도
weapon_speed = 1

# 폰트 정의
game_font = pygame.font.Font(None, 60)

# 게임 시간
total_time = 100
start_ticks = pygame.time.get_ticks()

# 이벤트 루프
running = True
while (running):
    # FPS
    dt = clock.tick(30)

    # 이벤트 처리
    for event in pygame.event.get():

        # 게임 종료
        if event.type == pygame.QUIT:
            running = False

        # 키 제어
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width - weapon_width) / 2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            elif event.key == pygame.K_SPACE:
                pass

    # 캐릭터 위치 업데이트
    character_x_pos += character_to_x * dt

    # 경계값 처리
    if character_x_pos <= 0:
        character_x_pos = 0
    elif character_x_pos >= screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed * dt] for w in weapons]
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 충돌 처리를 위한 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    
    # 충돌 처리
    

    #경과 시간 표시
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 초 단위
    timer = game_font.render(str(int(total_time - elapsed_time)), True, pygame.Color("White"))

    # 타임 오버
    if (total_time - elapsed_time) <= 0:
        print("Time Over")
        running = False

    # 화면에 불러오기
    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(timer, (screen_width / 2, 10))
   
    pygame.display.update()

# pygame 종료
pygame.time.delay(2000) # 2초 후 종료
pygame.quit()