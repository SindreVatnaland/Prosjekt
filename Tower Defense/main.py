import pygame, random, sys

pygame.mixer.pre_init(frequency=44100, size=32, channels=1, buffer=1024)
pygame.init()

width = 1280
height = 720

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

background_surface = pygame.transform.scale((pygame.image.load("assets/background.png").convert()), (width-350, height))
background_rect = background_surface.get_rect(topleft=(0,0))

rock_surface = pygame.image.load("assets/rock.jpg")
rock_rect = rock_surface.get_rect(bottomright=(width, height))

scale_enemy = (50, 50)
green_enemy_surface = pygame.transform.scale(pygame.image.load("assets/green_square.png"), scale_enemy)
yellow_enemy_surface = pygame.transform.scale(pygame.image.load("assets/yellow_square.png"), scale_enemy)
blue_enemy_surface = pygame.transform.scale(pygame.image.load("assets/blue_square.png"), scale_enemy)
orange_enemy_surface = pygame.transform.scale(pygame.image.load("assets/orange_square.png"), scale_enemy)
red_enemy_surface = pygame.transform.scale(pygame.image.load("assets/red_square.png"), scale_enemy)
enemy_rect = green_enemy_surface.get_rect(center=(-70, 100))

scale_turret = (70, 70)

mouse_upgrade_surface = pygame.transform.scale(pygame.image.load("assets/mouse.png"), (50, 60))
mouse_upgrade_rect = mouse_upgrade_surface.get_rect(center=(width - 350 * 1.7 / 5, 350))

green_turret_surface = pygame.transform.scale(pygame.image.load("assets/green_circle.png"), scale_turret)
baige_turret_surface = pygame.transform.scale(pygame.image.load("assets/baige_circle.png"), scale_turret)
blue_turret_surface = pygame.transform.scale(pygame.image.load("assets/blue_circle.png"), scale_turret)
red_turret_surface = pygame.transform.scale(pygame.image.load("assets/red_circle.png"), scale_turret)
turret_rect = green_turret_surface.get_rect(center=(width-350*3/4, 270))
turret2_rect = green_turret_surface.get_rect(center=(width-350*2/4, 270))
turret3_rect = green_turret_surface.get_rect(center=(width-350*1/4, 270))
nuke_rect = green_turret_surface.get_rect(center=(width-350*3/5, 350))
turret_rect_list = [turret_rect, turret2_rect, turret3_rect, nuke_rect, mouse_upgrade_rect]
turret_color_list = [green_turret_surface, red_turret_surface, blue_turret_surface]

shade_surface = pygame.transform.scale(pygame.image.load("assets/shade.png"), (300, 300))
shade_rect = shade_surface.get_rect(center=(width-350/2, 310))
shade_surface_small = pygame.transform.scale(pygame.image.load("assets/shade.png"), (300, 80))

#Hitboxes for map
line1 = pygame.Rect(0, 75, 260, 50)
line2 = pygame.Rect(210, 75, 50, 170)
line3 = pygame.Rect(210, 195, 200, 50)
line4 = pygame.Rect(355, 75, 50, 170)
line5 = pygame.Rect(355, 75, 200, 50)
line6 = pygame.Rect(520, 75, 50, 305)
line7 = pygame.Rect(355, 330, 200, 50)
line8 = pygame.Rect(355, 330, 50, 300)
line9 = pygame.Rect(355, 590, 210, 50)
line10 = pygame.Rect(525, 465, 50, 170)
line11 = pygame.Rect(525, 470, 200, 50)
line12 = pygame.Rect(675, 465, 50, 170)
line13 = pygame.Rect(675, 590, 250, 50)
lines_list = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13]

#Hitbox for setting direction to enemies
turn_rect1 = green_enemy_surface.get_rect(center=(280, 100))
turn_rect2 = green_enemy_surface.get_rect(center=(230, 268))
turn_rect3 = green_enemy_surface.get_rect(center=(428, 220))
turn_rect4 = green_enemy_surface.get_rect(center=(380, 50))
turn_rect5 = green_enemy_surface.get_rect(center=(590, 100))
turn_rect6 = green_enemy_surface.get_rect(center=(540, 405))
turn_rect7 = green_enemy_surface.get_rect(center=(340, 355))
turn_rect8 = green_enemy_surface.get_rect(center=(390, 660))
turn_rect9 = green_enemy_surface.get_rect(center=(595, 610))
turn_rect10 = green_enemy_surface.get_rect(center=(545, 440))
turn_rect11 = green_enemy_surface.get_rect(center=(750, 490))
turn_rect12 = green_enemy_surface.get_rect(center=(700, 660))

end_rect = green_enemy_surface.get_rect(center=(960, 610))

ENEMYSPAWN = pygame.USEREVENT + 0
pygame.time.set_timer(ENEMYSPAWN, 350)

TURRET1_ATTACK = pygame.USEREVENT + 1
pygame.time.set_timer(TURRET1_ATTACK, 2500)

TURRET2_ATTACK = pygame.USEREVENT + 2
pygame.time.set_timer(TURRET2_ATTACK, 1500)

TURRET3_ATTACK = pygame.USEREVENT + 3
pygame.time.set_timer(TURRET3_ATTACK, 3000)


class tower_defense:
    def __init__(self, width, height):
        self.game_over_font = pygame.font.Font("04B_19.TTF", 120)
        self.coins_font = pygame.font.Font("04B_19.TTF", 25)
        self.ready_font = pygame.font.Font("04B_19.TTF", 40)
        self.turret_font = pygame.font.Font("04B_19.TTF", 30)
        self.wave_font = pygame.font.Font("04B_19.TTF", 60)
        self.health_font = pygame.font.Font("04B_19.TTF", 30)
        self.high_score_font = pygame.font.Font("04B_19.TTF", 20)
        self.info_font = pygame.font.Font("04B_19.TTF", 20)

        high_score = open("high_score.txt", "r")
        self.high_score = int(high_score.readlines()[0])
        high_score.close()

        self.coins = 1500

        self.game_active = True
        self.ready = True

        self.width = width
        self.height = height

        self.health = 10
        self.speed = 3.5
        self.wave = 0
        self.click_damage = 1

        self.enemies_list = []
        self.enemies_on_screen = []
        self.enemy_state_list = []
        self.enemy_number = 0
        self.enemy_type_list = []

        self.turret_list = []
        self.turret_type_list = []
        self.turret_range_rect = []
        self.turret_attack_states = []

        self.turret1_prize = 100
        self.turret2_prize = 250
        self.turret3_prize = 500
        self.nuke_prize = 750
        self.mouse_prize = 500

        self.item_place_state = 0

        self.turn_collision_box_list = [turn_rect1, turn_rect2, turn_rect3, turn_rect4, turn_rect5, turn_rect6,
                                        turn_rect7, turn_rect8, turn_rect9, turn_rect10, turn_rect11, turn_rect12]


        self.play_game()

    def blit(self, mouse_pos, mouse_rect):
        display.blit(rock_surface, rock_rect)
        display.blit(background_surface, background_rect)
        display.blit(shade_surface, shade_rect)
        self.draw_items()
        self.text_display()
        self.draw_turrets()
        self.draw_item_hover(mouse_pos)
        self.draw_info_hover(mouse_rect, mouse_pos)
        self.draw_enemies()
        #pygame.draw.rect(display, (255, 0, 0), line10)
        return

    def place_turret(self, position):
        if self.item_place_state != 0:
            turret_rect = pygame.Rect(position[0]-37, position[1]-35, 70, 70)
            for line in lines_list:
                if line.colliderect(turret_rect):
                    return
            if position[0] < self.width-350-37:
                for line_rect in lines_list:
                    if turret_rect.colliderect(line_rect):
                        return
                for rect in self.turret_list:
                    if not turret_rect.colliderect(rect):
                        continue
                    else:
                        return
                self.turret_list.append(turret_rect)
                if self.item_place_state == 1 or self.item_place_state == 2:
                    self.turret_range_rect.append((pygame.Rect(position[0]-37-self.item_place_state*75,
                                                               position[1]-35-self.item_place_state*75,
                                                               70+2*self.item_place_state*75,
                                                               70+2*self.item_place_state*75)))
                elif self.item_place_state == 3:
                    self.turret_range_rect.append((pygame.Rect(position[0]-37-1*75, position[1]-35-1*75, 70+2*1*75, 70+2*1*75)))
                self.turret_type_list.append(self.item_place_state)
                self.turret_attack_states.append(0)
                self.item_place_state = 0
        return

    def upgrade_click_damage(self):
        if self.click_damage < 3:
            self.click_damage += 1
        else:
            self.coins += 1500
            return

    def nuke(self):
        for index, enemy in enumerate(self.enemies_on_screen):
            self.enemy_type_list[index] -= 3
            if self.enemy_type_list[index] <= 0:
                self.delete_enemy(index)

    def turret1_attack(self):
        for turret_index, turret in enumerate(self.turret_list):
            if self.turret_type_list[turret_index] == 1:
                for enemy_index, enemy in enumerate(self.enemies_on_screen):
                    if enemy.colliderect(self.turret_range_rect[turret_index]):
                        self.turret_attack_states[turret_index] = 1
                        self.enemy_type_list[enemy_index] -= 1
                        if self.enemy_type_list[enemy_index] <= 0:
                            self.delete_enemy(enemy_index)
                            break


    def turret2_attack(self):
        for turret_index, turret in enumerate(self.turret_list):
            if self.turret_type_list[turret_index] == 2:
                for enemy_index, enemy in enumerate(self.enemies_on_screen):
                    if enemy.colliderect(self.turret_range_rect[turret_index]):
                        self.turret_attack_states[turret_index] = 1
                        self.enemy_type_list[enemy_index] -= 2
                        if self.enemy_type_list[enemy_index] <= 0:
                            self.delete_enemy(enemy_index)
                            break

    def turret3_attack(self):
        for turret_index, turret in enumerate(self.turret_list):
            if self.turret_type_list[turret_index] == 3:
                for enemy_index, enemy in enumerate(self.enemies_on_screen):
                    if enemy.colliderect(self.turret_range_rect[turret_index]):
                        self.turret_attack_states[turret_index] = 1
                        self.enemy_type_list[enemy_index] -= 1
                        if self.enemy_type_list[enemy_index] <= 0:
                            self.delete_enemy(enemy_index)



    def create_enemies(self):
        for i in range(int(100*(self.wave*0.12))):
            self.enemies_list.append(enemy_rect)
            self.enemy_state_list.append(0)
            if i <= 10:
                self.enemy_type_list.append(1)
            elif i < 30:
                self.enemy_type_list.append(random.randint(1, 2))
            elif i < 50:
                self.enemy_type_list.append(random.randint(1, 3))
            elif i < 70:
                self.enemy_type_list.append(random.randint(2, 3))
            elif i < 100:
                self.enemy_type_list.append(random.randint(3, 4))
            else:
                self.enemy_type_list.append(random.randint(3, 5))
        return

    def draw_turrets(self):
        for index, turret in enumerate(self.turret_list):
            if self.turret_type_list[index] == 1:
                display.blit(green_turret_surface, self.turret_list[index])
            elif self.turret_type_list[index] == 2:
                display.blit(red_turret_surface, self.turret_list[index])
            elif self.turret_type_list[index] == 3:
                display.blit(blue_turret_surface, self.turret_list[index])
            elif self.turret_type_list[index] == 4:
                display.blit(baige_turret_surface, self.turret_list[index])
        for index, turret in enumerate(self.turret_range_rect):
            for enemy in self.enemies_on_screen:
                if turret.colliderect(enemy):
                    if self.turret_attack_states[index] == 1:
                        pygame.draw.rect(display, (255, 0, 0), turret, 2)
                        pygame.draw.rect(display, (255, 0, 0), self.turret_list[index], 2)
                        self.turret_attack_states[index] = 0
                    else:
                        pygame.draw.rect(display, (0, 0, 0), turret, 2)
                        pygame.draw.rect(display, (0, 0, 0), self.turret_list[index], 2)
                    break

        return

    def draw_items(self):
        display.blit(green_turret_surface, turret_rect)
        display.blit(red_turret_surface, turret2_rect)
        display.blit(blue_turret_surface, turret3_rect)
        display.blit(baige_turret_surface, nuke_rect)
        display.blit(mouse_upgrade_surface, mouse_upgrade_rect)
        return

    def draw_item_hover(self, mouse_pos):
        if self.item_place_state != 0:
            display.blit(turret_color_list[self.item_place_state-1], pygame.Rect(mouse_pos[0]-37, mouse_pos[1]-35, 70, 70))
            pygame.draw.rect(display, (0, 0, 0), (mouse_pos[0]-37, mouse_pos[1]-35, 70, 70), 2)
            if self.item_place_state == 1 or self.item_place_state == 2:
                pygame.draw.rect(display, (255, 0, 0), (mouse_pos[0]-37-self.item_place_state*75,
                                                        mouse_pos[1]-35-self.item_place_state*75,
                                                        70+2*self.item_place_state*75,
                                                        70+2*self.item_place_state*75), 2)
            elif self.item_place_state == 3:
                pygame.draw.rect(display, (255, 0, 0), (mouse_pos[0]-37-1*75, mouse_pos[1]-35-1*75, 70+2*1*75, 70+2*1*75), 2)
        else:
            return

    def draw_enemies(self):
        for i, enemy in enumerate(self.enemies_on_screen):
            self.move_enemy(enemy, i)
            if self.enemy_number == 0:
                continue
            elif self.enemy_type_list[i] == 1:
                display.blit(green_enemy_surface, enemy)
            elif self.enemy_type_list[i] == 2:
                display.blit(yellow_enemy_surface, enemy)
            elif self.enemy_type_list[i] == 3:
                display.blit(blue_enemy_surface, enemy)
            elif self.enemy_type_list[i] == 4:
                display.blit(orange_enemy_surface, enemy)
            elif self.enemy_type_list[i] == 5:
                display.blit(red_enemy_surface, enemy)
        return

    def move_enemy(self, enemy, index):
        if not self.check_turn_collision(enemy, index):
            if self.enemy_number >= 1:
                if self.enemy_state_list[index] == 0:
                    enemy.centerx += self.speed
                elif self.enemy_state_list[index] == 1:
                    enemy.centery += self.speed
                elif self.enemy_state_list[index] == 2:
                    enemy.centerx -= self.speed
                else:
                    enemy.centery -= self.speed
        return True

    def check_turn_collision(self, enemy, index):
        for i, box in enumerate(self.turn_collision_box_list):
            if box.colliderect(enemy):
                if i in [1, 3, 7, 9, 11]:
                    self.enemy_state_list[index] = 0
                elif i in [0, 4, 6, 10]:
                    self.enemy_state_list[index] = 1
                elif i == 5:
                    self.enemy_state_list[index] = 2
                else:
                    self.enemy_state_list[index] = 3
            else:
                if self.check_collision_end(enemy, index):
                    return False
        return

    def check_collision_end(self, enemy, index):
        if end_rect.colliderect(enemy):
            self.health -= self.enemy_type_list[index]
            self.delete_enemy(index)
            self.check_game_over()
            return True
        return

    def check_click_collision(self, mouse_rect, mouse_pos):
        if self.item_place_state != 0:
            self.place_turret(mouse_pos)
            return
        elif mouse_rect.colliderect(turret_rect):
            if self.coins >= self.turret1_prize and self.coins > 0:
                self.coins -= self.turret1_prize
                self.item_place_state = 1
            return
        elif mouse_rect.colliderect(turret2_rect):
            if self.coins >= self.turret2_prize and self.coins > 0:
                self.coins -= self.turret2_prize
                self.item_place_state = 2
            return
        elif mouse_rect.colliderect(turret3_rect):
            if self.coins >= self.turret3_prize and self.coins > 0:
                self.coins -= self.turret3_prize
                self.item_place_state = 3
            return
        elif mouse_rect.colliderect(nuke_rect):
            if self.coins >= self.nuke_prize and self.coins > 0:
                self.coins -= self.nuke_prize
                self.nuke()
                self.item_place_state = 0
            return
        elif mouse_rect.colliderect(mouse_upgrade_rect):
            if self.coins >= self.mouse_prize and self.coins > 0:
                self.coins -= self.mouse_prize
                self.mouse_prize += 1000
                self.item_place_state = 0
                self.upgrade_click_damage()
            return

        for index, turret in enumerate(self.turret_list):
            if mouse_rect.colliderect(turret):
                self.item_place_state = self.turret_type_list[index]
                self.delete_turret(index)
                break
        for index, enemy in enumerate(self.enemies_on_screen):
            if mouse_rect.colliderect(enemy):
                self.enemy_type_list[index] -= self.click_damage
                if self.enemy_type_list[index] <= 0:
                    self.delete_enemy(index)
                    break
        return

    def delete_turret(self, index):
        del self.turret_list[index]
        del self.turret_type_list[index]
        del self.turret_range_rect[index]
        return

    def delete_enemy(self, index):
        del self.enemy_type_list[index]
        del self.enemies_on_screen[index]
        del self.enemy_state_list[index]
        del self.enemies_list[index]
        self.enemy_number -= 1
        self.coins += 1
        return

    def update_high_score(self):
        high_score = open("high_score.txt", "w")
        high_score.write(str(self.wave))
        high_score.close()

    def check_game_over(self):
        if self.health <= 0:
            self.game_active = False
        return

    def text_display(self):
        wave_outline_surface = self.wave_font.render(f"Wave: {self.wave}", True, (0, 0, 0)).convert_alpha()
        wave_surface = self.wave_font.render(f"Wave: {self.wave}", True, (255, 255, 255)).convert_alpha()
        wave_rect = wave_surface.get_rect(midtop=(self.width-(350/2), 50))
        display.blit(wave_outline_surface, wave_rect)
        wave_rect.centerx -= 3
        wave_rect.centery -= 3
        display.blit(wave_surface, wave_rect)

        high_score_outline_surface = self.high_score_font.render(f"High score: {self.high_score}", True, (0, 0, 0)).convert_alpha()
        high_score_surface = self.high_score_font.render(f"High score: {self.high_score}", True, (255, 255, 255)).convert_alpha()
        high_score_rect = high_score_surface.get_rect(midtop=(self.width-(350/2), 15))
        display.blit(high_score_outline_surface, high_score_rect)
        high_score_rect.centerx -= 3
        high_score_rect.centery -= 3
        display.blit(high_score_surface, high_score_rect)

        turret_outline_surface = self.turret_font.render(f"Turrets", True, (0, 0, 0)).convert_alpha()
        turret_surface = self.turret_font.render(f"Turrets", True, (255, 255, 255)).convert_alpha()
        turret_rect = turret_surface.get_rect(midtop=(self.width-(350/2), 180))
        display.blit(turret_outline_surface, turret_rect)
        turret_rect.centerx -= 3
        turret_rect.centery -= 3
        display.blit(turret_surface, turret_rect)

        health_outline_surface = self.health_font.render(f"Health: {self.health}", True, (0, 0, 0)).convert_alpha()
        health_surface = self.health_font.render(f"Health: {self.health}", True, (255, 255, 255)).convert_alpha()
        health_rect = health_surface.get_rect(midtop=(self.width-(350/2), 670))
        display.blit(health_outline_surface, health_rect)
        health_rect.centerx -= 3
        health_rect.centery -= 3
        display.blit(health_surface, health_rect)

        coins_outline_surface = self.coins_font.render(f"Coins: {self.coins}", True, (0, 0, 0)).convert_alpha()
        coins_surface = self.coins_font.render(f"Coins: {self.coins}", True, (255, 255, 255)).convert_alpha()
        coins_rect = coins_surface.get_rect(midtop=(self.width-(350/2), 480))
        display.blit(coins_outline_surface, coins_rect)
        coins_rect.centerx -= 3
        coins_rect.centery -= 3
        display.blit(coins_surface, coins_rect)
        return

    def draw_info_hover(self, mouse_rect, mouse_pos):
        for index, item in enumerate(turret_rect_list):
            if item.colliderect(mouse_rect) and mouse_pos[0] > self.width-350:
                if index == 0:
                    display.blit(shade_surface_small, shade_surface_small.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1])))
                    prize_outline_surface = self.info_font.render(f"Prize: {self.turret1_prize}", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Prize: {self.turret1_prize}", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+5))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Cooldown: 2500", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Cooldown: 2500", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+30))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Attack: One enemy at once", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Attack: One enemy at once", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+55))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                elif index == 1:
                    display.blit(shade_surface_small, shade_surface_small.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1])))
                    prize_outline_surface = self.info_font.render(f"Prize: {self.turret2_prize}", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Prize: {self.turret2_prize}", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+5))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Cooldown: 1500", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Cooldown: 1500", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+30))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Attack: One enemy at once", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Attack: One enemy at once", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+55))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                elif index == 2:
                    display.blit(shade_surface_small, shade_surface_small.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1])))
                    prize_outline_surface = self.info_font.render(f"Prize: {self.turret3_prize}", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Prize: {self.turret3_prize}", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+5))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Cooldown: 3000", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Cooldown: 3000", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+30))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Attack: Multiple enemies at once", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Attack: Multiple enemies at once", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+55))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                elif index == 3:
                    display.blit(shade_surface_small, shade_surface_small.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1])))
                    prize_outline_surface = self.info_font.render(f"Prize: {self.nuke_prize}", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Prize: {self.nuke_prize}", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+5))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Cooldown: 0", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Cooldown: 0", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+30))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Deals 3 damage to every enemy", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Deals 3 damage to every enemy", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+55))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                elif index == 4:
                    display.blit(shade_surface_small, shade_surface_small.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1])))
                    prize_outline_surface = self.info_font.render(f"Prize: {self.mouse_prize}", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Prize: {self.mouse_prize}", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+5))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Upgrade mouse damage by 1", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Upgrade mouse damage by 1", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+30))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)
                    prize_outline_surface = self.info_font.render(f"Max damage: 3", True, (0, 0, 0)).convert_alpha()
                    prize_surface = self.info_font.render(f"Max damage: 3", True, (255, 255, 255)).convert_alpha()
                    prize_rect = prize_surface.get_rect(topright=(mouse_pos[0]-5, mouse_pos[1]+55))
                    display.blit(prize_outline_surface, prize_rect)
                    prize_rect.centerx -= 3
                    prize_rect.centery -= 3
                    display.blit(prize_surface, prize_rect)

        return

    def draw_ready(self):
        ready_outline_surface = self.ready_font.render(f"Press 'Space' when ready", True, (0, 0, 0)).convert_alpha()
        ready_surface = self.ready_font.render(f"Press 'Space' when ready", True, (255, 255, 255)).convert_alpha()
        ready_rect = ready_surface.get_rect(midtop=((self.width-350)/2, 150))
        display.blit(ready_outline_surface, ready_rect)
        ready_rect.centerx -= 3
        ready_rect.centery -= 3
        display.blit(ready_surface, ready_rect)

        tip_outline_surface = self.info_font.render(f"Tips:", True, (0, 0, 0)).convert_alpha()
        tip_surface = self.info_font.render(f"Tips:", True, (255, 255, 255)).convert_alpha()
        tip_rect = tip_surface.get_rect(topleft=(20, 650))
        display.blit(tip_outline_surface, tip_rect)
        tip_rect.centerx -= 3
        tip_rect.centery -= 3
        display.blit(tip_surface, tip_rect)

        tip1_outline_surface = self.info_font.render(f"Click on enemies to deal damage", True, (0, 0, 0)).convert_alpha()
        tip1_surface = self.info_font.render(f"Click on enemies to deal damage", True, (255, 255, 255)).convert_alpha()
        tip1_rect = tip1_surface.get_rect(topleft=(20, 670))
        display.blit(tip1_outline_surface, tip1_rect)
        tip1_rect.centerx -= 3
        tip1_rect.centery -= 3
        display.blit(tip1_surface, tip1_rect)

        tip2_outline_surface = self.info_font.render(f"Sell items by select and right click", True, (0, 0, 0)).convert_alpha()
        tip2_surface = self.info_font.render(f"Sell items by select and right click", True, (255, 255, 255)).convert_alpha()
        tip2_rect = tip2_surface.get_rect(topleft=(20, 690))
        display.blit(tip2_outline_surface, tip2_rect)
        tip2_rect.centerx -= 3
        tip2_rect.centery -= 3
        display.blit(tip2_surface, tip2_rect)
        return

    def draw_game_over(self):
        game_over_outline_surface = self.game_over_font.render(f"Game Over", True, (0, 0, 0)).convert_alpha()
        game_over_surface = self.game_over_font.render(f"Game Over", True, (255, 255, 255)).convert_alpha()
        game_over_rect = game_over_surface.get_rect(midtop=((self.width-350)/2, 150))
        display.blit(game_over_outline_surface, game_over_rect)
        game_over_rect.centerx -= 3
        game_over_rect.centery -= 3
        display.blit(game_over_surface, game_over_rect)
        return

    def play_game(self):
        while True:
            mouse = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse[0]-3, mouse[1]-3, 5, 5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.check_click_collision(mouse_rect, mouse)
                    if event.button == 3 and self.item_place_state != 0:
                        if self.item_place_state == 1:
                            self.coins += 100
                        elif self.item_place_state == 2:
                            self.coins += 200
                        elif self.item_place_state == 3:
                            self.coins += 500
                        self.item_place_state = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.health = 10
                        self.speed = 4
                        self.wave = 0
                        self.enemies_list = []
                        self.enemies_on_screen = []
                        self.enemy_state_list = []
                        self.enemy_number = 0
                        self.enemy_type_list = []
                        self.turret_list = []
                        self.turret_type_list = []
                        self.turret_range_rect = []
                        self.turret_attack_states = []
                        self.game_active = True
                        self.ready = True
                    if event.key == pygame.K_SPACE and not self.ready:
                        self.coins += int((self.wave * 100)**0.4+10)
                        self.wave += 1
                        if self.speed < 12:
                            self.speed = 3 + self.wave**0.6
                            if self.speed >= 10:
                                self.speed = 10
                        print(self.speed)
                        self.enemies_list = []
                        self.enemies_on_screen = []
                        self.enemy_state_list = []
                        self.enemy_number = 0
                        self.enemy_type_list = []
                        self.create_enemies()
                        self.health += 5
                        if self.wave > self.high_score:
                            self.high_score = self.wave
                        self.game_active = True
                        self.ready = True
                if event.type == ENEMYSPAWN:
                    if len(self.enemies_on_screen) < len(self.enemies_list):
                        self.enemies_on_screen.append(self.enemies_list[self.enemy_number].copy())
                        self.enemy_number += 1
                if event.type == TURRET1_ATTACK:
                    self.turret_attack_state = 1
                    self.turret1_attack()
                if event.type == TURRET2_ATTACK:
                    self.turret_attack_state = 1
                    self.turret2_attack()
                if event.type == TURRET3_ATTACK:
                    self.turret_attack_state = 1
                    self.turret3_attack()

            if self.game_active:
                self.blit(mouse, mouse_rect)
                if len(self.enemies_list) <= 0:
                    self.draw_ready()
                    self.ready = False
            else:
                if self.wave >= self.high_score:
                    self.update_high_score()
                    self.high_score = self.wave
                self.draw_game_over()
            pygame.time.Clock().tick(40)
            pygame.display.update()

if __name__ == '__main__':
    game = tower_defense(width, height)
