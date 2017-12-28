
import gamebox
import pygame
import random

camera = gamebox.Camera(1000, 1000)

player = gamebox.from_color(50, 50, "white", 20, 20)

sun = gamebox.from_color(500, 500, "yellow", 40, 40)

enemy = gamebox.from_color(1500, -500, "green", 25, 25)
enemy2 = gamebox.from_color(-500, 1500, "green", 25, 25)

borders = [gamebox.from_color(500, -600, "white", 2500, 200), gamebox.from_color(500, 1600, "white", 2500, 200),
          gamebox.from_color(-600, 500, "white", 200, 2500), gamebox.from_color(1600, 500, "white", 200, 2500)]

score = 0
level = 0
start_timer = 0
game_on = False
can_bomb = False
explosion_timer = 0
reset_timer = 0
current_explosion = False

def tick(keys):
   global score
   global level
   global game_on
   global start_timer
   global can_bomb
   global explosion_timer
   global current_explosion
   global reset_timer

   current_score = gamebox.from_text(500, 950, "Score: " + str(score), "Arial", 80, "white", True)

   if level == 0:
       camera.clear('black')
       camera.draw(gamebox.from_text(500,500,"Welcome to Worbit","Arial", 100, "White", True))
       start_timer += 1
       if start_timer == 120:
           level += 1
   camera.display()

   if level == 1:
       camera.clear('black')

       if game_on:
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

           if player.touches(sun):
               gamebox.pause()

           if player.touches(enemy):
               gamebox.pause()

           if enemy.touches(sun):
               score += 1
               number = random.randint(1, 4)
               if number == 1:
                   enemy.center = [-100, -100]
               if number == 2:
                   enemy.center = [1100, -100]
               if number == 3:
                   enemy.center = [1100, 1100]
               if number == 4:
                   enemy.center = [-100, 1100]

           for border in borders:
               player.move_to_stop_overlapping(border)

           if score == 5:
               level += 1

           if can_bomb == False:
               reset_timer += 1
               if reset_timer == 180:
                   reset_timer = 0
                   can_bomb = True

           if can_bomb:
               if pygame.K_SPACE in keys:
                   global explosion
                   explosion = gamebox.from_color(player.x, player.y, "blue", 20, 20)
                   current_explosion = True
                   camera.draw(explosion)
                   can_bomb = False

           if current_explosion:
               explosion.width += 3
               camera.draw(explosion)
               if enemy.touches(explosion):
                   score += 1
                   number = random.randint(1, 4)
                   if number == 1:
                       enemy.center = [-100, -100]
                   if number == 2:
                       enemy.center = [1100, -100]
                   if number == 3:
                       enemy.center = [1100, 1100]
                   if number == 4:
                       enemy.center = [-100, 1100]
               explosion_timer += 1
               if explosion_timer == 30:
                   explosion_timer = 0
                   current_explosion = False

       if pygame.K_SPACE in keys:
           game_on = True

       for border in borders:
           camera.draw(border)
       camera.draw(sun)
       camera.draw(player)
       camera.draw(enemy)
       camera.draw(current_score)

   if level == 2:
       camera.clear('black')

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

       if player.touches(sun):
           gamebox.pause()

       if player.touches(enemy):
           gamebox.pause()

       if player.touches(enemy2):
           gamebox.pause()

       if enemy.touches(sun):
           score += 1
           number = random.randint(1, 4)
           if number == 1:
               enemy.center = [-100, -100]
           if number == 2:
               enemy.center = [1100, -100]
           if number == 3:
               enemy.center = [1100, 1100]
           if number == 4:
               enemy.center = [-100, 1100]

       if enemy2.touches(sun):
           score += 1
           number = random.randint(1, 4)
           if number == 1:
               enemy2.center = [-100, -100]
           if number == 2:
               enemy2.center = [1100, -100]
           if number == 3:
               enemy2.center = [1100, 1100]
           if number == 4:
               enemy2.center = [-100, 1100]

       if can_bomb == False:
           reset_timer += 1
           if reset_timer == 180:
               reset_timer = 0
               can_bomb = True

       if can_bomb:
           if pygame.K_SPACE in keys:
               explosion = gamebox.from_color(player.x, player.y, "blue", 20, 20)
               current_explosion = True
               camera.draw(explosion)
               can_bomb = False

       if current_explosion:
           explosion.width += 3
           camera.draw(explosion)
           if enemy.touches(explosion):
               score += 1
               number = random.randint(1, 4)
               if number == 1:
                   enemy.center = [-100, -100]
               if number == 2:
                   enemy.center = [1100, -100]
               if number == 3:
                   enemy.center = [1100, 1100]
               if number == 4:
                   enemy.center = [-100, 1100]
           if enemy2.touches(explosion):
               score += 1
               number = random.randint(1, 4)
               if number == 1:
                   enemy2.center = [-100, -100]
               if number == 2:
                   enemy2.center = [1100, -100]
               if number == 3:
                   enemy2.center = [1100, 1100]
               if number == 4:
                   enemy2.center = [-100, 1100]
           explosion_timer += 1
           if explosion_timer == 30:
               explosion_timer = 0
               current_explosion = False

       for border in borders:
           player.move_to_stop_overlapping(border)

       for border in borders:
           camera.draw(border)
       camera.draw(sun)
       camera.draw(player)
       camera.draw(enemy)
       camera.draw(enemy2)
       camera.draw(current_score)

ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)
