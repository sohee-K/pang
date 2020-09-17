import os
import pygame

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
character_pos_x = (screen_width - character_width) / 2
character_pos_y = screen_height - character_height - stage_height

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

# 공 불러오기
ball = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))
]

balls = []

# 공의 최초 속도
ball_init_speed = [-18, -15, -12, -9]

# 최초의 공 추가
balls.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "init_speed_y" : ball_init_speed[0]
})

# 사라질 공과 무기
ball_to_remove = -1
weapon_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 60)

# 게임 시간
total_time = 100
start_ticks = pygame.time.get_ticks()

# 게임 종료 메시지
game_result = "Game Clear"

# 이벤트 루프
running = True
while running:
    # FPS
    dt = clock.tick(30)

    # 이벤트 처리
    for event in pygame.event.get():

        # 게임 종료
        if event.type == pygame.QUIT:
            running = False
            break

        # 키 제어
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_pos_x = character_pos_x + (character_width - weapon_width) / 2
                weapon_pos_y = character_pos_y
                weapons.append([weapon_pos_x, weapon_pos_y])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 캐릭터 위치 업데이트
    character_pos_x += character_to_x * dt

    # 경계값 처리
    if character_pos_x <= 0:
        character_pos_x = 0
    elif character_pos_x >= screen_width - character_width:
        character_pos_x = screen_width - character_width

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed * dt] for w in weapons]
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 조정
    for ball_idx, ball_val in enumerate(balls):
        ball_img_idx = ball_val["img_idx"]
        ball_size = ball[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 경계값 및 속도 처리
        if ball_val["pos_x"] <= 0 or ball_val["pos_x"] >= screen_width - ball_width:
            ball_val["to_x"] = - ball_val["to_x"]
        if ball_val["pos_y"] >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]
        else:
            ball_val["to_y"] += 0.5

        # 공 위치 업데이트
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 충돌 처리
    # 공 정보 업데이트
    for ball_idx, ball_val in enumerate(balls):
        ball_img_idx = ball_val["img_idx"]
        ball_rect = ball[ball_img_idx].get_rect()
        ball_rect.left = ball_val["pos_x"]
        ball_rect.top = ball_val["pos_y"]

        # 캐릭터 정보 업데이트
        character_rect = character.get_rect()
        character_rect.left = character_pos_x
        character_rect.top = character_pos_y

        # 캐릭터와 공의 충돌 처리
        if character_rect.colliderect(ball_rect):
            game_result = "Game Over"
            running = False
            break

        # 무기 정보 업데이트
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_val[0]
            weapon_rect.top = weapon_val[1]

            # 무기와 공의 충돌 처리
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # 가장 작은 공이 아닐 경우, 작은 공 2개 추가
                if ball_img_idx < 3:

                    # 현재 공 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 작은 공 정보
                    s_ball_rect = ball[ball_img_idx + 1].get_rect()
                    s_ball_width = s_ball_rect.size[0]
                    s_ball_height = s_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 공
                    balls.append({
                        "pos_x" : ball_val["pos_x"] + (ball_width - s_ball_width) / 2,
                        "pos_y" : ball_val["pos_y"] + (ball_height - s_ball_height) / 2,
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : -3,
                        "to_y" : -6,
                        "init_speed_y" : ball_init_speed[ball_img_idx + 1]
                    })

                    # 오른쪽으로 튕겨나가는 공
                    balls.append({
                        "pos_x" : ball_val["pos_x"] + (ball_width - s_ball_width) / 2,
                        "pos_y" : ball_val["pos_y"] + (ball_height - s_ball_height) / 2,
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : 3,
                        "to_y" : -6,
                        "init_speed_y" : ball_init_speed[ball_img_idx + 1]
                    })

                break
             
        # 이중 for문 빠져나가기
        else:
            continue
        break
    
    # 충돌한 무기와 공 없애기
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    # 공을 모두 없앤 경우
    if len(balls) == 0:
        running = False
        break

    #경과 시간 표시
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 초 단위
    timer = game_font.render("TIME : {}".format(int(total_time - elapsed_time)), True, pygame.Color("White"))

    # 타임 오버
    if (total_time - elapsed_time) <= 0:
        game_result = "Time Over"
        running = False
        break

    # 화면에 불러오기
    screen.blit(background, (0, 0))
    for weapon_pos_x, weapon_pos_y in weapons:
        screen.blit(weapon, (weapon_pos_x, weapon_pos_y))
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img = ball[val["img_idx"]]
        screen.blit(ball_img, (ball_pos_x, ball_pos_y))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_pos_x, character_pos_y))
    screen.blit(timer, (10, 10))

    pygame.display.update()

# 게임 종료 메세지 출력
game_msg = game_font.render(game_result, True, pygame.Color("White"))
game_msg_rect = game_msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(game_msg, game_msg_rect)
pygame.display.update()

# pygame 종료
pygame.time.delay(2000) # 2초 후 종료
pygame.quit()
