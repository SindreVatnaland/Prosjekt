import pygame, sys, random

pygame.mixer.pre_init(frequency = 44100, size = 32, channels = 1, buffer = 1024)
pygame.init()

width = 576

height = 1024

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

background_surface = pygame.transform.scale2x(pygame.image.load("assets/background-day.png").convert())
floor_surface = pygame.transform.scale2x(pygame.image.load("assets/base.png").convert())
pipe_surface = pygame.transform.scale2x(pygame.image.load("assets/pipe-green.png").convert_alpha())


bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha())


game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/gameover.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(width/2, height/2))

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
swoosh_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
die_sound = pygame.mixer.Sound("sound/sfx_die.wav")


PIPESPAWN = pygame.USEREVENT
pygame.time.set_timer(PIPESPAWN, 1500)

BIRD_ANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_ANIMATION, 150)

POINTSPAWN = pygame.USEREVENT + 2
pygame.time.set_timer(POINTSPAWN, 1500)

class Flappy_Bird:
    def __init__(self, width, height):

        self.score_font = pygame.font.Font("04B_19.TTF", 60)
        self.high_score_font = pygame.font.Font("04B_19.TTF", 40)


        self.bird_animation_index = 0
        self.bird_frames = [bird_downflap, bird_midflap, bird_upflap]
        self.bird_surface = self.bird_frames[self.bird_animation_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, height/2))

        self.width = width
        self.height = height
        self.floor_posx = 0
        self.floor_posy = 900
        self.pipe_list = []
        self.point_rect_list = []
        self.bird_speed = 0
        self.bird_movement = 0
        self.gravity = 0.5

        self.score = 0
        self.high_score = 0
        high_score = open("high_score.txt", "r")
        self.high_score = int(high_score.readlines()[0])
        high_score.close()


        self.game_status = True

        self.play_game()



    def blit(self):
        display.blit(background_surface, (0, 0))
        self.draw_bird()
        self.draw_pipes()
        self.move_point_rect()
        self.roll_floor()

    def draw_bird(self):
        self.update_movement()
        bird_frames = pygame.transform.rotozoom(self.bird_surface, -self.bird_movement*2.5, 1)
        display.blit(bird_frames, self.bird_rect)

    def update_movement(self):
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

    def create_point_rect(self):
        point_rect = pipe_surface.get_rect(midtop=(700, 100))
        return point_rect

    def move_point_rect(self):
        if len(self.point_rect_list) < 3:
            for rect in self.point_rect_list:
                rect.centerx -= 4
        else:
            for rect in self.point_rect_list[-3:]:
                rect.centerx -= 4




    def create_pipes(self):
        random_height = 700-random.randint(0, 15)*20
        bot_pipe = pipe_surface.get_rect(midtop=(650, random_height))
        top_pipe = pipe_surface.get_rect(midbottom=(650, random_height - 200))
        return bot_pipe, top_pipe

    def move_pipes(self):
        if len(self.pipe_list) < 6:
            for pipe in self.pipe_list:
                pipe.centerx -= 4

        else:
            for pipe in self.pipe_list[-6:]:
                pipe.centerx -= 4


    def draw_pipes(self):
        self.move_pipes()
        if len(self.pipe_list) < 6:
            for pipe_rect in self.pipe_list:
                if pipe_rect.bottom >= 1024:
                    display.blit(pipe_surface, pipe_rect)
                else:
                    flip = pygame.transform.flip(pipe_surface, False, True)
                    display.blit(flip, pipe_rect)
        else:
            for pipe_rect in self.pipe_list[-6:]:
                if pipe_rect.bottom >= 1024:
                    display.blit(pipe_surface, pipe_rect)
                else:
                    flip = pygame.transform.flip(pipe_surface, False, True)
                    display.blit(flip, pipe_rect)



    def roll_floor(self):
        display.blit(floor_surface, (self.floor_posx, self.floor_posy))
        if self.floor_posx <= -48:
            self.floor_posx = 0
        self.floor_posx -= 4



    def check_collition(self):
        if len(self.pipe_list) < 6:
            for pipe_rect in self.pipe_list:
                if self.bird_rect.colliderect(pipe_rect):
                    die_sound.play()
                    return False
        else:
            for pipe_rect in self.pipe_list[-6:]:
                if self.bird_rect.colliderect(pipe_rect):
                    die_sound.play()
                    return False
        if self.bird_rect.bottom >= self.floor_posy or self.bird_rect.top <= -100:
            die_sound.play()
            return False

        return True



    def check_point(self):
        if len(self.point_rect_list) < 3:
            for i, point_rect in enumerate(self.point_rect_list):
                if self.bird_rect.colliderect(point_rect):
                    del self.point_rect_list[i]
                    return True
        else:
            for i, point_rect in enumerate(self.point_rect_list[-3:]):
                if self.bird_rect.colliderect(point_rect):
                    del self.point_rect_list[i]
                    return True
        return False

    def update_high_score(self):
        high_score = open("high_score.txt", "w")
        high_score.write(str(self.score))
        high_score.close()

    def score_display(self, status=None):
        if status == "game over":
            high_score_outline_surface = self.high_score_font.render(f"High score: {self.high_score}", True, (0, 0, 0))
            high_score_surface = self.high_score_font.render(f"High score: {self.high_score}", True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(self.width/2, 800))
            display.blit(high_score_outline_surface, high_score_rect)
            high_score_rect.centerx -= 3
            high_score_rect.centery -= 3
            display.blit(high_score_surface, high_score_rect)
        score_outline_surface = self.score_font.render(f"{self.score}", True, (0, 0, 0))
        score_surface = self.score_font.render(f"{self.score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(midtop=(self.width/2, 100))
        display.blit(score_outline_surface, score_rect)
        score_rect.centerx -= 3
        score_rect.centery -= 3
        display.blit(score_surface, score_rect)

    def play_game(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        flap_sound.play()
                        self.bird_movement = -9
                    if event.key == pygame.K_SPACE and not self.game_status:
                        flap_sound.play()
                        self.bird_movement = -9
                        self.bird_rect.centery = 500
                        self.score = 0
                        self.pipe_list.clear()
                        self.point_rect_list.clear()
                        self.game_status = True
                if event.type == PIPESPAWN:
                    self.pipe_list.extend(self.create_pipes())
                if event.type == POINTSPAWN:
                    self.point_rect_list.append(self.create_point_rect())
                if event.type == BIRD_ANIMATION:
                    if self.bird_animation_index >= 2:
                        self.bird_animation_index = 0
                    else:
                        self.bird_animation_index += 1
                    self.bird_surface = self.bird_frames[self.bird_animation_index]



            if self.game_status:
                if not self.check_collition():
                    self.game_status = False
                else:
                    if self.check_point():
                        point_sound.play()
                        self.score += 1
                    self.blit()
                self.score_display()
            else:
                if self.score > self.high_score:
                    self.update_high_score()
                    self.high_score = self.score
                display.blit(game_over_surface, game_over_rect)
                self.score_display("game over")


            pygame.time.Clock().tick(60)
            pygame.display.update()





if __name__ == '__main__':
    game = Flappy_Bird(width, height)