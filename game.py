# Galen Palowitch - gdp5st
# Garrett Vercoe - grv9ff

# All graphics are original content
# Sounds are free source

import gamebox
import pygame
import random

camera = gamebox.Camera(1000, 1000)

player_sprite = gamebox.load_sprite_sheet("Player spritesheet.png", 1, 10)
player = gamebox.from_image(50, 50, player_sprite[0])
player.width = 50

sun_sprite = gamebox.load_sprite_sheet("Sun change sprite.png", 1, 4)
sun = gamebox.from_image(500, 500, sun_sprite[0])
sun.width = 180

stars_sprite = gamebox.load_sprite_sheet("Star Sprite Sheet.png", 1, 5)
stars = gamebox.from_image(500, 500, stars_sprite[0])
stars_count = 0

enemy_sprite = gamebox.load_sprite_sheet("enemy sprite.png", 1, 6)
enemy = gamebox.from_image(1500, -500, enemy_sprite[0])
enemy.width = 50

enemy2 = gamebox.from_image(-500, 1500, enemy_sprite[0])
enemy2.width = 50

enemy3 = gamebox.from_image(1500, 1500, enemy_sprite[0])
enemy3.width = 50

enemy_boss_sprite = gamebox.load_sprite_sheet("ENEMY BOSS KING.png", 1, 4)
enemy_boss = gamebox.from_image(-500, -500, enemy_boss_sprite[0])
enemy_boss.width = 160

borders = [gamebox.from_color(500, -600, "white", 2500, 200), gamebox.from_color(500, 1600, "white", 2500, 200),
           gamebox.from_color(-600, 500, "white", 200, 2500), gamebox.from_color(1600, 500, "white", 200, 2500)]

explosion_sprite = gamebox.load_sprite_sheet("Spritesheet Explosion.png", 1, 6)

meter_sprite = gamebox.load_sprite_sheet("fuel meter.png", 1, 7)
meter = gamebox.from_image(910, 950, meter_sprite[0])
meter.width = 160

loading = gamebox.load_sprite_sheet("loading.png", 1, 3)
loading_image = gamebox.from_image(500, 700, loading[0])

meteor_sprite = gamebox.load_sprite_sheet('meteor sprite.png', 1, 6)
meteor = gamebox.from_image(1500, 0, meteor_sprite[0])
meteor.width = 80

music = gamebox.load_sound('Broke_For_Free_-_01_-_Night_Owl.ogg')
explosion_sound = gamebox.load_sound('SEFY - Explosion Sound Effect - 1.ogg')

score = 0
level = 0
start_timer = 0
game_on = False
can_bomb = False
explosion_timer = 0
reset_timer = 0
current_explosion = False
game_timer = 0
player_timer = 0
sun_timer = 0
boss_beat = False
enemy_dead = False
enemy2_dead = False
enemy3_dead = False
meteor_shower = False
sun_rage = False
boss_health = 40
boss = False
paused = False


def enemy_reset(enemy_name):
    global score
    score += 1
    number = random.randint(1, 4)
    if number == 1:
        enemy_name.center = [-100, -100]
    if number == 2:
        enemy_name.center = [1100, -100]
    if number == 3:
        enemy_name.center = [1100, 1100]
    if number == 4:
        enemy_name.center = [-100, 1100]


def meteor_set():
    number = random.randint(1, 8)
    if number == 1:
        meteor.center = [-500, 0]
    if number == 2:
        meteor.center = [0, -500]
    if number == 3:
        meteor.center = [0, 1500]
    if number == 4:
        meteor.center = [1500, 0]
    if number == 5:
        meteor.center = [1000, -500]
    if number == 6:
        meteor.center = [1500, 1000]
    if number == 7:
        meteor.center = [1000, 1500]
    if number == 8:
        meteor.center = [-500, 1000]


def tick(keys):
    global score
    global level
    global game_on
    global start_timer
    global can_bomb
    global explosion_timer
    global current_explosion
    global reset_timer
    global stars_count
    global game_timer
    global player_timer
    global sun_timer
    global boss_beat
    global enemy_dead
    global enemy2_dead
    global enemy3_dead
    global meteor_shower
    global sun_rage
    global boss_health
    global boss
    global paused


    if level == 0:
    # Loading Screen
        camera.clear('black')
        camera.draw(gamebox.from_image(500, 500, "Welcome Screen.png"))
        camera.draw(gamebox.from_image(500, 900, "names.png"))

        image_index = int(start_timer) % 2
        camera.draw(gamebox.from_image(500, 700, loading[image_index]))

        start_timer += 0.2
        if start_timer > 20:
            level += 1
            music.play(-1)

    if level == 1:
        camera.clear('black')
        camera.draw(gamebox.from_image(500, 500, "Static Background Screen.png"))

        current_score = gamebox.from_text(100, 970, "SCORE: " + str(score), "Century Gothic", 30, 'White', True)

        if not game_on:
            camera.draw(gamebox.from_image(500, 300, "press space.png"))
            camera.draw(gamebox.from_image(500, 800, "DIRECTIONS.png"))

        if game_on:
        # Stars
            star_index = int(stars_count) % 5
            camera.draw(gamebox.from_image(500, 500, stars_sprite[star_index]))
            stars_count += 0.25

            game_timer += 1

            if game_timer < 60:
                camera.draw(gamebox.from_image(500, 800, "DIRECTIONS.png"))
        # Meteor
            if game_timer % 900 == 0:
                meteor_shower = True

            if meteor_shower:
                meteor_distance = round(((meteor.x - sun.x) ** 2 + (meteor.y - sun.y) ** 2) ** (1 / 2))

                meteor.speedy += 0.1 * (meteor.y - sun.y) / meteor_distance
                meteor.speedx += 0.1 * (meteor.x - sun.x) / meteor_distance

                meteor.y -= meteor.speedy
                meteor.x -= meteor.speedx

                meteor_index = int(game_timer) % 6
                meteor.image = meteor_sprite[meteor_index]

                if enemy.touches(meteor, -20, -20):
                    enemy_reset(enemy)

                if player.touches(meteor, -20, -20):
                    gamebox.pause()
                    paused = True

                if meteor.touches(sun, -70, -50):
                    meteor_shower = False
                    meteor.speedx = 0
                    meteor.speedy = 0
                    meteor_set()
                    sun_rage = True

                camera.draw(meteor)

            if sun_rage:
                sun_index = int(sun_timer) % 4
                sun.image = sun_sprite[sun_index]
                sun_timer += 1
                if sun_index == 0:
                    sun.width += 1
                if sun_timer == 30:
                    sun_timer = 0
                    sun.image = sun_sprite[0]
                    sun_rage = False

        # Movement
            player_distance = round(((player.x - sun.x) ** 2 + (player.y - sun.y) ** 2) ** (1 / 2))

            player.speedy += 1 * (player.y - sun.y) / player_distance
            player.speedx += 1 * (player.x - sun.x) / player_distance

            if pygame.K_UP in keys:
                player.speedy += .5
            if pygame.K_DOWN in keys:
                player.speedy -= .5
            if pygame.K_LEFT in keys:
                player.speedx += .5
            if pygame.K_RIGHT in keys:
                player.speedx -= .5

            player.y -= player.speedy
            player.x -= player.speedx

            enemy_distance = round(((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2) ** (1 / 2))
            enemy.speedy = 5 * (enemy.y - player.y) / enemy_distance
            enemy.speedx = 5 * (enemy.x - player.x) / enemy_distance

            enemy.y -= enemy.speedy
            enemy.x -= enemy.speedx

            player_index = int(player_timer) % 10
            player.image = player_sprite[player_index]
            enemy_index = int(player_timer) % 6
            enemy.image = enemy_sprite[enemy_index]

            player_timer += 0.1

        # Interactions between player, enemy, and sun
            if player.touches(sun, -70, -50):
                gamebox.pause()
                paused = True

            if player.touches(enemy, -30, -30):
                gamebox.pause()
                paused = True

            if enemy.touches(sun, -70, -50):
                enemy_reset(enemy)

            for border in borders:
                player.move_to_stop_overlapping(border)

        # Explosions
            if not can_bomb:
                if reset_timer == 1:
                    meter.image = meter_sprite[0]
                if reset_timer == 30:
                    meter.image = meter_sprite[1]
                if reset_timer == 60:
                    meter.image = meter_sprite[2]
                if reset_timer == 90:
                    meter.image = meter_sprite[3]
                if reset_timer == 120:
                    meter.image = meter_sprite[4]
                if reset_timer == 150:
                    meter.image = meter_sprite[5]
                if reset_timer == 180:
                    meter.image = meter_sprite[6]
                    reset_timer = 0
                    can_bomb = True
                reset_timer += 1

            if can_bomb:
                if pygame.K_SPACE in keys:
                    global explosion
                    explosion = gamebox.from_image(player.x, player.y, explosion_sprite[0])
                    explosion_sound.play()
                    current_explosion = True
                    can_bomb = False

            if current_explosion:
                camera.draw(explosion)
                explosion_timer += 1
                if explosion_timer == 2:
                    explosion.image = explosion_sprite[1]
                    if enemy.touches(explosion, -100, -100):
                        enemy_reset(enemy)
                if explosion_timer == 4:
                    explosion.image = explosion_sprite[2]
                    if enemy.touches(explosion, -80, -80):
                        enemy_reset(enemy)
                if explosion_timer == 7:
                    explosion.image = explosion_sprite[3]
                    if enemy.touches(explosion, -60, -60):
                        enemy_reset(enemy)
                if explosion_timer == 12:
                    explosion.image = explosion_sprite[4]
                    if enemy.touches(explosion, -40, -40):
                        enemy_reset(enemy)
                if explosion_timer == 20:
                    explosion.image = explosion_sprite[5]
                    if enemy.touches(explosion, -30, -30):
                        enemy_reset(enemy)

                if explosion_timer == 30:
                    explosion_timer = 0
                    current_explosion = False

            if score == 5:
                level += 1

    # Drawing
        for border in borders:
            camera.draw(border)
        camera.draw(sun)
        camera.draw(player)
        camera.draw(enemy)
        camera.draw(current_score)
        camera.draw(meter)

    # Start Game
        if pygame.K_SPACE in keys:
            game_on = True

    if level == 2:
        camera.clear('black')
        camera.draw(gamebox.from_image(500, 500, "Static Background Screen.png"))

        current_score = gamebox.from_text(100, 970, "SCORE: " + str(score), "Century Gothic", 30, 'White', True)

    # Stars
        star_index = int(stars_count) % 5
        camera.draw(gamebox.from_image(500, 500, stars_sprite[star_index]))
        stars_count += 0.25

        game_timer += 1

# Meteor
        if game_timer % 900 == 0:
            meteor_shower = True

        if meteor_shower:
            meteor_distance = round(((meteor.x - sun.x) ** 2 + (meteor.y - sun.y) ** 2) ** (1 / 2))

            meteor.speedy += 0.1 * (meteor.y - sun.y) / meteor_distance
            meteor.speedx += 0.1 * (meteor.x - sun.x) / meteor_distance

            meteor.y -= meteor.speedy
            meteor.x -= meteor.speedx

            meteor_index = int(game_timer) % 6
            meteor.image = meteor_sprite[meteor_index]

            if enemy.touches(meteor, -20, -20):
                enemy_reset(enemy)

            if enemy2.touches(meteor, -20, -20):
                enemy_reset(enemy2)

            if player.touches(meteor, -20, -20):
                gamebox.pause()
                paused = True

            if meteor.touches(sun, -70, -50):
                meteor_shower = False
                meteor.speedx = 0
                meteor.speedy = 0
                meteor_set()
                sun_rage = True

            camera.draw(meteor)

        if sun_rage:
            sun_index = int(sun_timer) % 4
            sun.image = sun_sprite[sun_index]
            sun_timer += 1
            if sun_index == 0:
                sun.width += 1
            if sun_timer == 30:
                sun.image = sun_sprite[0]
                sun_timer = 0
                sun_rage = False

    # Movement
        player_distance = round(((player.x - sun.x) ** 2 + (player.y - sun.y) ** 2) ** (1 / 2))

        player.speedy += 1 * (player.y - sun.y) / player_distance
        player.speedx += 1 * (player.x - sun.x) / player_distance

        if pygame.K_UP in keys:
            player.speedy += .5
        if pygame.K_DOWN in keys:
            player.speedy -= .5
        if pygame.K_LEFT in keys:
            player.speedx += .5
        if pygame.K_RIGHT in keys:
            player.speedx -= .5

        player.y -= player.speedy
        player.x -= player.speedx

        enemy_distance = round(((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2) ** (1 / 2))
        enemy.speedy = 5 * (enemy.y - player.y) / enemy_distance
        enemy.speedx = 5 * (enemy.x - player.x) / enemy_distance

        enemy2_distance = round(((enemy2.x - player.x) ** 2 + (enemy2.y - player.y) ** 2) ** (1 / 2))
        enemy2.speedy = 5 * (enemy2.y - player.y) / enemy2_distance
        enemy2.speedx = 5 * (enemy2.x - player.x) / enemy2_distance

        enemy.y -= enemy.speedy
        enemy.x -= enemy.speedx

        enemy2.y -= enemy2.speedy
        enemy2.x -= enemy2.speedx

        player_index = int(player_timer) % 10
        player.image = player_sprite[player_index]
        enemy_index = int(player_timer) % 6
        enemy.image = enemy_sprite[enemy_index]
        enemy2.image = enemy_sprite[enemy_index]

        player_timer += 0.1

    # Interactions between player, enemy, and sun
        if player.touches(sun, -70, -50):
            gamebox.pause()
            paused = True

        if player.touches(enemy, -30, -30):
            gamebox.pause()
            paused = True

        if player.touches(enemy2, -30, -30):
            gamebox.pause()
            paused = True

        if enemy.touches(sun, -70, -50):
            enemy_reset(enemy)

        if enemy2.touches(sun, -70, -50):
            enemy_reset(enemy2)

        for border in borders:
            player.move_to_stop_overlapping(border)

    # Explosions
        if not can_bomb:
            if reset_timer == 1:
                meter.image = meter_sprite[0]
            if reset_timer == 30:
                meter.image = meter_sprite[1]
            if reset_timer == 60:
                meter.image = meter_sprite[2]
            if reset_timer == 90:
                meter.image = meter_sprite[3]
            if reset_timer == 120:
                meter.image = meter_sprite[4]
            if reset_timer == 150:
                meter.image = meter_sprite[5]
            if reset_timer == 180:
                meter.image = meter_sprite[6]
                reset_timer = 0
                can_bomb = True
            reset_timer += 1

        if can_bomb:
            if pygame.K_SPACE in keys:
                explosion = gamebox.from_image(player.x, player.y, explosion_sprite[0])
                explosion_sound.play()
                current_explosion = True
                can_bomb = False

        if current_explosion:
            camera.draw(explosion)
            explosion_timer += 1
            if explosion_timer == 2:
                explosion.image = explosion_sprite[1]
                if enemy.touches(explosion, -100, -100):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -100, -100):
                    enemy_reset(enemy2)
            if explosion_timer == 4:
                explosion.image = explosion_sprite[2]
                if enemy.touches(explosion, -80, -80):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -80, -80):
                    enemy_reset(enemy2)
            if explosion_timer == 7:
                explosion.image = explosion_sprite[3]
                if enemy.touches(explosion, -60, -60):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -60, -60):
                    enemy_reset(enemy2)
            if explosion_timer == 12:
                explosion.image = explosion_sprite[4]
                if enemy.touches(explosion, -40, -40):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -40, -40):
                    enemy_reset(enemy2)
            if explosion_timer == 20:
                explosion.image = explosion_sprite[5]
                if enemy.touches(explosion, -30, -30):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -30, -30):
                    enemy_reset(enemy2)

            if explosion_timer == 30:
                explosion_timer = 0
                current_explosion = False

        for border in borders:
            camera.draw(border)
        camera.draw(sun)
        camera.draw(player)
        camera.draw(enemy)
        camera.draw(enemy2)
        camera.draw(current_score)
        camera.draw(meter)
    # Score
        if score == 15:
            level += 1

    if level == 3:
        camera.clear('black')
        camera.draw(gamebox.from_image(500, 500, "Static Background Screen.png"))

        current_score = gamebox.from_text(100, 970, "SCORE: " + str(score), "Century Gothic", 30, 'White', True)

        star_index = int(stars_count) % 5
        camera.draw(gamebox.from_image(500, 500, stars_sprite[star_index]))
        stars_count += 0.25

        game_timer += 1

        if game_timer % 900 == 0:
            meteor_shower = True

        if meteor_shower:
            meteor_distance = round(((meteor.x - sun.x) ** 2 + (meteor.y - sun.y) ** 2) ** (1 / 2))

            meteor.speedy += 0.1 * (meteor.y - sun.y) / meteor_distance
            meteor.speedx += 0.1 * (meteor.x - sun.x) / meteor_distance

            meteor.y -= meteor.speedy
            meteor.x -= meteor.speedx

            meteor_index = int(game_timer) % 6
            meteor.image = meteor_sprite[meteor_index]

            if enemy.touches(meteor, -20, -20):
                enemy_reset(enemy)

            if enemy2.touches(meteor, -20, -20):
                enemy_reset(enemy2)

            if enemy3.touches(meteor, -20, -20):
                enemy_reset(enemy3)

            if player.touches(meteor, -20, -20):
                gamebox.pause()
                paused = True

            if meteor.touches(sun, -70, -50):
                meteor_shower = False
                meteor.speedx = 0
                meteor.speedy = 0
                meteor_set()
                sun_rage = True

            camera.draw(meteor)

        if sun_rage:
            sun_index = int(sun_timer) % 4
            sun.image = sun_sprite[sun_index]
            sun_timer += 1
            if sun_index == 0:
                sun.width += 1
            if sun_timer == 30:
                sun_timer = 0
                sun.image = sun_sprite[0]
                sun_rage = False

    # Movement
        player_distance = round(((player.x - sun.x) ** 2 + (player.y - sun.y) ** 2) ** (1 / 2))

        player.speedy += 1 * (player.y - sun.y) / player_distance
        player.speedx += 1 * (player.x - sun.x) / player_distance

        if pygame.K_UP in keys:
            player.speedy += .5
        if pygame.K_DOWN in keys:
            player.speedy -= .5
        if pygame.K_LEFT in keys:
            player.speedx += .5
        if pygame.K_RIGHT in keys:
            player.speedx -= .5

        player.y -= player.speedy
        player.x -= player.speedx

        enemy_distance = round(((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2) ** (1 / 2))
        enemy.speedy = 5 * (enemy.y - player.y) / enemy_distance
        enemy.speedx = 5 * (enemy.x - player.x) / enemy_distance

        enemy2_distance = round(((enemy2.x - player.x) ** 2 + (enemy2.y - player.y) ** 2) ** (1 / 2))
        enemy2.speedy = 5 * (enemy2.y - player.y) / enemy2_distance
        enemy2.speedx = 5 * (enemy2.x - player.x) / enemy2_distance

        enemy3_distance = round(((enemy3.x - player.x) ** 2 + (enemy3.y - player.y) ** 2) ** (1 / 2))
        enemy3.speedy = 5 * (enemy3.y - player.y) / enemy3_distance
        enemy3.speedx = 5 * (enemy3.x - player.x) / enemy3_distance

        enemy.y -= enemy.speedy
        enemy.x -= enemy.speedx

        enemy2.y -= enemy2.speedy
        enemy2.x -= enemy2.speedx

        enemy3.y -= enemy3.speedy
        enemy3.x -= enemy3.speedx

        player_index = int(player_timer) % 10
        player.image = player_sprite[player_index]
        enemy_index = int(player_timer) % 6
        enemy.image = enemy_sprite[enemy_index]
        enemy2.image = enemy_sprite[enemy_index]
        enemy3.image = enemy_sprite[enemy_index]

        player_timer += 0.1

    # Interactions between player, enemy, and sun
        if player.touches(sun, -70, -50):
            gamebox.pause()
            paused = True

        if player.touches(enemy, -30, -30):
            gamebox.pause()
            paused = True

        if player.touches(enemy2, -30, -30):
            gamebox.pause()
            paused = True

        if player.touches(enemy3, -30, -30):
            gamebox.pause()
            paused = True

        if enemy.touches(sun, -70, -50):
            enemy_reset(enemy)

        if enemy2.touches(sun, -70, -50):
            enemy_reset(enemy2)

        if enemy3.touches(sun, -70, -50):
            enemy_reset(enemy3)

        for border in borders:
            player.move_to_stop_overlapping(border)

    # Explosions
        if not can_bomb:
            if reset_timer == 1:
                meter.image = meter_sprite[0]
            if reset_timer == 30:
                meter.image = meter_sprite[1]
            if reset_timer == 60:
                meter.image = meter_sprite[2]
            if reset_timer == 90:
                meter.image = meter_sprite[3]
            if reset_timer == 120:
                meter.image = meter_sprite[4]
            if reset_timer == 150:
                meter.image = meter_sprite[5]
            if reset_timer == 180:
                meter.image = meter_sprite[6]
                reset_timer = 0
                can_bomb = True
            reset_timer += 1

        if can_bomb:
            if pygame.K_SPACE in keys:
                explosion = gamebox.from_image(player.x, player.y, explosion_sprite[0])
                current_explosion = True
                explosion_sound.play()
                can_bomb = False

        if current_explosion:
            camera.draw(explosion)
            explosion_timer += 1
            if explosion_timer == 2:
                explosion.image = explosion_sprite[1]
                if enemy.touches(explosion, -100, -100):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -100, -100):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -100, -100):
                    enemy_reset(enemy3)
            if explosion_timer == 4:
                explosion.image = explosion_sprite[2]
                if enemy.touches(explosion, -80, -80):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -80, -80):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -80, -80):
                    enemy_reset(enemy3)
            if explosion_timer == 7:
                explosion.image = explosion_sprite[3]
                if enemy.touches(explosion, -60, -60):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -60, -60):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -60, -60):
                    enemy_reset(enemy3)
            if explosion_timer == 12:
                explosion.image = explosion_sprite[4]
                if enemy.touches(explosion, -40, -40):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -40, -40):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -40, -40):
                    enemy_reset(enemy3)
            if explosion_timer == 20:
                explosion.image = explosion_sprite[5]
                if enemy.touches(explosion, -30, -30):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -30, -30):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -30, -30):
                    enemy_reset(enemy3)

            if explosion_timer == 30:
                explosion_timer = 0
                current_explosion = False

        for border in borders:
            camera.draw(border)
        camera.draw(sun)
        camera.draw(player)
        camera.draw(enemy)
        camera.draw(enemy2)
        camera.draw(enemy3)
        camera.draw(current_score)
        camera.draw(meter)

                # Score
        if score == 27:
            level += 1

    if level == 4:
        camera.clear('black')
        camera.draw(gamebox.from_image(500, 500, "Static Background Screen.png"))

        current_score = gamebox.from_text(100, 970, "SCORE: " + str(score), "Century Gothic", 30, 'White', True)

        star_index = int(stars_count) % 5
        camera.draw(gamebox.from_image(500, 500, stars_sprite[star_index]))
        stars_count += 0.25

        game_timer += 1

        if game_timer % 900 == 0:
            meteor_shower = True

        if meteor_shower:
            meteor_distance = round(((meteor.x - sun.x) ** 2 + (meteor.y - sun.y) ** 2) ** (1 / 2))

            meteor.speedy += 0.1 * (meteor.y - sun.y) / meteor_distance
            meteor.speedx += 0.1 * (meteor.x - sun.x) / meteor_distance

            meteor.y -= meteor.speedy
            meteor.x -= meteor.speedx

            meteor_index = int(game_timer) % 6
            meteor.image = meteor_sprite[meteor_index]

            if enemy.touches(meteor, -20, -20):
                enemy_reset(enemy)

            if enemy2.touches(meteor, -20, -20):
                enemy_reset(enemy2)

            if enemy3.touches(meteor, -20, -20):
                enemy_reset(enemy3)

            if player.touches(meteor, -20, -20):
                gamebox.pause()
                paused = True

            if meteor.touches(sun, -70, -50):
                meteor_shower = False
                meteor.speedx = 0
                meteor.speedy = 0
                meteor_set()
                sun_rage = True

            camera.draw(meteor)

        if sun_rage:
            sun_index = int(sun_timer) % 4
            if sun_index == 0:
                sun.width += 1
            sun.image = sun_sprite[sun_index]
            sun_timer += 1

            if sun_timer == 30:
                sun_timer = 0
                sun.image = sun_sprite[0]
                sun_rage = False

            # Movement
        player_distance = round(((player.x - sun.x) ** 2 + (player.y - sun.y) ** 2) ** (1 / 2))

        player.speedy += 1 * (player.y - sun.y) / player_distance
        player.speedx += 1 * (player.x - sun.x) / player_distance

        if pygame.K_UP in keys:
            player.speedy += .5
        if pygame.K_DOWN in keys:
            player.speedy -= .5
        if pygame.K_LEFT in keys:
            player.speedx += .5
        if pygame.K_RIGHT in keys:
            player.speedx -= .5

        player.y -= player.speedy
        player.x -= player.speedx

        if not enemy_dead:
            enemy_distance = round(((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2) ** (1 / 2))
            enemy.speedy = 5 * (enemy.y - player.y) / enemy_distance
            enemy.speedx = 5 * (enemy.x - player.x) / enemy_distance

            enemy.y -= enemy.speedy
            enemy.x -= enemy.speedx

            if player.touches(enemy, -30, -30):
                gamebox.pause()
                paused = True

        if not enemy2_dead:
            enemy2_distance = round(((enemy2.x - player.x) ** 2 + (enemy2.y - player.y) ** 2) ** (1 / 2))
            enemy2.speedy = 5 * (enemy2.y - player.y) / enemy2_distance
            enemy2.speedx = 5 * (enemy2.x - player.x) / enemy2_distance

            enemy2.y -= enemy2.speedy
            enemy2.x -= enemy2.speedx

            if player.touches(enemy2, -30, -30):
                gamebox.pause()
                paused = True

        if not enemy3_dead:
            enemy3_distance = round(((enemy3.x - player.x) ** 2 + (enemy3.y - player.y) ** 2) ** (1 / 2))
            enemy3.speedy = 5 * (enemy3.y - player.y) / enemy3_distance
            enemy3.speedx = 5 * (enemy3.x - player.x) / enemy3_distance

            enemy3.y -= enemy3.speedy
            enemy3.x -= enemy3.speedx

            if player.touches(enemy3, -30, -30):
                gamebox.pause()
                paused = True

        if enemy_dead and enemy2_dead and enemy3_dead:
            enemy_boss_distance = round(((enemy_boss.x - player.x) ** 2 + (enemy_boss.y - player.y) ** 2) ** (1 / 2))
            enemy_boss.speedy = 7 * (enemy_boss.y - player.y) / enemy_boss_distance
            enemy_boss.speedx = 7 * (enemy_boss.x - player.x) / enemy_boss_distance

            enemy_boss.y -= enemy_boss.speedy
            enemy_boss.x -= enemy_boss.speedx

            if player.touches(enemy_boss, -60, -60):
                gamebox.pause()
                paused = True

        player_index = int(player_timer) % 10
        player.image = player_sprite[player_index]
        enemy_index = int(player_timer) % 6
        enemy.image = enemy_sprite[enemy_index]
        enemy2.image = enemy_sprite[enemy_index]
        enemy3.image = enemy_sprite[enemy_index]
        enemy_boss_index = int(player_timer) % 4
        enemy_boss.image = enemy_boss_sprite[enemy_boss_index]

        player_timer += 0.1

    # Interactions between player, enemy, and sun
        if player.touches(sun, -70, -50):
            gamebox.pause()
            paused = True

        if enemy.touches(sun, -70, -50):
            enemy_dead = True
            enemy_reset(enemy)

        if enemy2.touches(sun, -70, -50):
            enemy2_dead = True
            enemy_reset(enemy2)

        if enemy3.touches(sun, -70, -50):
            enemy3_dead = True
            enemy_reset(enemy3)

        for border in borders:
            player.move_to_stop_overlapping(border)

    # Explosions
        if not can_bomb:
            if reset_timer == 1:
                meter.image = meter_sprite[0]
            if reset_timer == 30:
                meter.image = meter_sprite[1]
            if reset_timer == 60:
                meter.image = meter_sprite[2]
            if reset_timer == 90:
                meter.image = meter_sprite[3]
            if reset_timer == 120:
                meter.image = meter_sprite[4]
            if reset_timer == 150:
                meter.image = meter_sprite[5]
            if reset_timer == 180:
                meter.image = meter_sprite[6]
                reset_timer = 0
                can_bomb = True
            reset_timer += 1

        if can_bomb:
            if pygame.K_SPACE in keys:
                explosion = gamebox.from_image(player.x, player.y, explosion_sprite[0])
                explosion_sound.play()
                current_explosion = True
                can_bomb = False

        if current_explosion:
            camera.draw(explosion)
            explosion_timer += 1
            if explosion_timer == 2:
                explosion.image = explosion_sprite[1]
                if enemy.touches(explosion, -100, -100):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -100, -100):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -100, -100):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -100, -100):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 4:
                explosion.image = explosion_sprite[2]
                if enemy.touches(explosion, -80, -80):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -80, -80):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -80, -80):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -80, -80):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 7:
                explosion.image = explosion_sprite[3]
                if enemy.touches(explosion, -60, -60):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -60, -60):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -60, -60):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -60, -60):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 12:
                explosion.image = explosion_sprite[4]
                if enemy.touches(explosion, -40, -40):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -40, -40):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -40, -40):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -40, -40):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 20:
                explosion.image = explosion_sprite[5]
                if enemy.touches(explosion, -30, -30):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -30, -30):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -30, -30):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -30, -30):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True

            if explosion_timer == 30:
                explosion_timer = 0
                current_explosion = False

    # Drawing
        for border in borders:
            camera.draw(border)
        camera.draw(sun)
        camera.draw(player)
        camera.draw(enemy)
        camera.draw(enemy2)
        camera.draw(enemy3)
        camera.draw(enemy_boss)
        camera.draw(current_score)
        camera.draw(meter)
    # Score
        if boss_beat:
            enemy_dead = False
            enemy2_dead = False
            enemy3_dead = False
            boss.center = [-500, -500]
            level += 1

    if level == 5:
        camera.clear('black')
        camera.draw(gamebox.from_image(500, 500, "Static Background Screen.png"))

        current_score = gamebox.from_text(100, 970, "SCORE: " + str(score), "Century Gothic", 30, 'White', True)

        star_index = int(stars_count) % 5
        camera.draw(gamebox.from_image(500, 500, stars_sprite[star_index]))
        stars_count += 0.25

        game_timer += 1

        if score % 25 == 0:
            boss = True

        if game_timer % 900 == 0:
            meteor_shower = True

        if meteor_shower:
            meteor_distance = round(((meteor.x - sun.x) ** 2 + (meteor.y - sun.y) ** 2) ** (1 / 2))

            meteor.speedy += 0.1 * (meteor.y - sun.y) / meteor_distance
            meteor.speedx += 0.1 * (meteor.x - sun.x) / meteor_distance

            meteor.y -= meteor.speedy
            meteor.x -= meteor.speedx

            meteor_index = int(game_timer) % 6
            meteor.image = meteor_sprite[meteor_index]

            if enemy.touches(meteor, -20, -20):
                enemy_reset(enemy)

            if enemy2.touches(meteor, -20, -20):
                enemy_reset(enemy2)

            if enemy3.touches(meteor, -20, -20):
                enemy_reset(enemy3)

            if player.touches(meteor, -20, -20):
                gamebox.pause()
                paused = True

            if meteor.touches(sun, -70, -50):
                meteor_shower = False
                meteor.speedx = 0
                meteor.speedy = 0
                meteor_set()
                sun_rage = True

            camera.draw(meteor)

        if sun_rage:
            sun_index = int(sun_timer) % 4
            if sun_index == 0:
                sun.width += 1
            sun.image = sun_sprite[sun_index]
            sun_timer += 1

            if sun_timer == 30:
                sun_timer = 0
                sun.image = sun_sprite[0]
                sun_rage = False

                # Movement
        player_distance = round(((player.x - sun.x) ** 2 + (player.y - sun.y) ** 2) ** (1 / 2))

        player.speedy += 1 * (player.y - sun.y) / player_distance
        player.speedx += 1 * (player.x - sun.x) / player_distance

        if pygame.K_UP in keys:
            player.speedy += .5
        if pygame.K_DOWN in keys:
            player.speedy -= .5
        if pygame.K_LEFT in keys:
            player.speedx += .5
        if pygame.K_RIGHT in keys:
            player.speedx -= .5

        player.y -= player.speedy
        player.x -= player.speedx

        enemy_distance = round(((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2) ** (1 / 2))
        enemy.speedy = 5 * (enemy.y - player.y) / enemy_distance
        enemy.speedx = 5 * (enemy.x - player.x) / enemy_distance

        enemy.y -= enemy.speedy
        enemy.x -= enemy.speedx

        if player.touches(enemy, -30, -30):
            gamebox.pause()
            paused = True

        enemy2_distance = round(((enemy2.x - player.x) ** 2 + (enemy2.y - player.y) ** 2) ** (1 / 2))
        enemy2.speedy = 5 * (enemy2.y - player.y) / enemy2_distance
        enemy2.speedx = 5 * (enemy2.x - player.x) / enemy2_distance

        enemy2.y -= enemy2.speedy
        enemy2.x -= enemy2.speedx

        if player.touches(enemy2, -30, -30):
            gamebox.pause()
            paused = True

        enemy3_distance = round(((enemy3.x - player.x) ** 2 + (enemy3.y - player.y) ** 2) ** (1 / 2))
        enemy3.speedy = 5 * (enemy3.y - player.y) / enemy3_distance
        enemy3.speedx = 5 * (enemy3.x - player.x) / enemy3_distance

        enemy3.y -= enemy3.speedy
        enemy3.x -= enemy3.speedx

        if player.touches(enemy3, -30, -30):
            gamebox.pause()
            paused = True

        player_index = int(player_timer) % 10
        player.image = player_sprite[player_index]
        enemy_index = int(player_timer) % 6
        enemy.image = enemy_sprite[enemy_index]
        enemy2.image = enemy_sprite[enemy_index]
        enemy3.image = enemy_sprite[enemy_index]

        if boss:
            enemy_boss_distance = round(((enemy_boss.x - player.x) ** 2 + (enemy_boss.y - player.y) ** 2) ** (1 / 2))
            enemy_boss.speedy = 7 * (enemy_boss.y - player.y) / enemy_boss_distance
            enemy_boss.speedx = 7 * (enemy_boss.x - player.x) / enemy_boss_distance

            enemy_boss.y -= enemy_boss.speedy
            enemy_boss.x -= enemy_boss.speedx

            if player.touches(enemy_boss, -60, -60):
                gamebox.pause()
                paused = True

            enemy_boss_index = int(player_timer) % 4
            enemy_boss.image = enemy_boss_sprite[enemy_boss_index]

        player_timer += 0.1

        # Interactions between player, enemy, and sun
        if player.touches(sun, -70, -50):
            gamebox.pause()
            paused = True

        if enemy.touches(sun, -70, -50):
            enemy_dead = True
            enemy_reset(enemy)

        if enemy2.touches(sun, -70, -50):
            enemy2_dead = True
            enemy_reset(enemy2)

        if enemy3.touches(sun, -70, -50):
            enemy3_dead = True
            enemy_reset(enemy3)

        for border in borders:
            player.move_to_stop_overlapping(border)

            # Explosions
        if not can_bomb:
            if reset_timer == 1:
                meter.image = meter_sprite[0]
            if reset_timer == 30:
                meter.image = meter_sprite[1]
            if reset_timer == 60:
                meter.image = meter_sprite[2]
            if reset_timer == 90:
                meter.image = meter_sprite[3]
            if reset_timer == 120:
                meter.image = meter_sprite[4]
            if reset_timer == 150:
                meter.image = meter_sprite[5]
            if reset_timer == 180:
                meter.image = meter_sprite[6]
                reset_timer = 0
                can_bomb = True
            reset_timer += 1

        if can_bomb:
            if pygame.K_SPACE in keys:
                explosion = gamebox.from_image(player.x, player.y, explosion_sprite[0])
                explosion_sound.play()
                current_explosion = True
                can_bomb = False

        if current_explosion:
            camera.draw(explosion)
            explosion_timer += 1
            if explosion_timer == 2:
                explosion.image = explosion_sprite[1]
                if enemy.touches(explosion, -100, -100):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -100, -100):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -100, -100):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -100, -100):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 4:
                explosion.image = explosion_sprite[2]
                if enemy.touches(explosion, -80, -80):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -80, -80):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -80, -80):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -80, -80):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 7:
                explosion.image = explosion_sprite[3]
                if enemy.touches(explosion, -60, -60):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -60, -60):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -60, -60):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -60, -60):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 12:
                explosion.image = explosion_sprite[4]
                if enemy.touches(explosion, -40, -40):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -40, -40):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -40, -40):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -40, -40):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True
            if explosion_timer == 20:
                explosion.image = explosion_sprite[5]
                if enemy.touches(explosion, -30, -30):
                    enemy_reset(enemy)
                if enemy2.touches(explosion, -30, -30):
                    enemy_reset(enemy2)
                if enemy3.touches(explosion, -30, -30):
                    enemy_reset(enemy3)
                if enemy_boss.touches(explosion, -30, -30):
                    boss_health -= 1
                    if boss_health == 0:
                        boss_beat = True

            if explosion_timer == 30:
                explosion_timer = 0
                current_explosion = False

                # Drawing
        for border in borders:
            camera.draw(border)
        camera.draw(sun)
        camera.draw(player)
        camera.draw(enemy)
        camera.draw(enemy2)
        camera.draw(enemy3)
        camera.draw(enemy_boss)
        camera.draw(current_score)
        camera.draw(meter)
        # Score
        if boss_beat:
            boss.center = [-500, -500]
            boss = False

    camera.display()

ticks_per_second = 30

meteor_set()
gamebox.timer_loop(ticks_per_second, tick)