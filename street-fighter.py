import pygame
from pygame import mixer

pygame.init()  # call all the features in pygame package

clock = pygame.time.Clock()
fps = 60

# game window
screen_width = 1200
screen_height = 450

screen = pygame.display.set_mode((screen_width, screen_height))  # set the size the the game window
pygame.display.set_caption('Street Fighter')  # setting the title for the game window
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# background music
mixer.music.load('sounds/background music.mp3')
mixer.music.play(-1)
jump_sound = mixer.Sound('sounds/jump.mp3')
punch_sound = mixer.Sound('sounds/attack/punch.mp3')
kick_sound = mixer.Sound('sounds/attack/kick.mp3')
power1_sound = mixer.Sound('sounds/attack/power 1.mp3')
power2_sound = mixer.Sound('sounds/attack/power 2.mp3')

# load images
# background image

class Background:
    def __init__(self):
        """Set components to manage multiple frames of the background"""
        self.background_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            bg = pygame.image.load(f'background/{i}.gif')
            scale = screen_width / bg.get_width()
            bg = pygame.transform.scale(bg, (bg.get_width() * scale, bg.get_height() * scale))
            self.background_list.append(bg)
        self.background_img = self.background_list[self.frame_index]

    def update(self):
        """Update images for the animation"""
        animation_cooldown = 100
        # handle animation
        # update images
        self.background_img = self.background_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.background_list):
                self.frame_index = 0

    def draw(self):
        """Draw the background"""
        screen.blit(self.background_img, (0, 0))


# fighter class
class Fighter:
    def __init__(self, x, y, name, img_scale, special_sound):
        self.name = name
        self.max_hp = 500
        self.hp = 500
        self.alive = True
        self.action = 'idle'
        self.scale = img_scale  # scale to adjust the size of the character image
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        self.frame_index = 0
        self.x = x  # Position of fighter respect to x axis
        self.y = y  # Position of fighter respect to y axis
        self.speed = 10
        self.jump = False
        self.in_air = False
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.special_sound = special_sound

    def move(self, move_left, move_right):  # method for moving left and right
        """Method for character movement left, right"""
        if move_left and self.x >= 0:  # check move and set boundary so the image won't move outside the screen
            self.x -= self.speed
            self.flip = True
        if move_right and self.x <= screen_width - self.image.get_width() - self.speed:
            self.x += self.speed
            self.flip = False

    def jumping(self):
        """Method for jump"""
        jump_step = 0
        GRAVITY = 0.3
        if first_fighter.jump and self.in_air == False:
            self.action = 'jump'
            self.draw()
            jump_sound.play()
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20
        jump_step += self.vel_y

        # check collision with floor
        if self.y + jump_step > 250:
            jump_step = 250 - self.y
            self.in_air = False
        # update rectangle position
        self.y += jump_step

    def draw(self):  # draw the character
        """Draw the fighter"""
        img = pygame.image.load(f'char_img/{self.name}/{self.action}.gif')
        self.image = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.x, self.y))

    def attack(self):
        if self.action == 'punch':
            punch_sound.play()
            self.draw()
        if self.action == 'kick':
            kick_sound.play()
            self.draw()
        if self.action == 'special_power':
            self.special_sound.play()
            self.draw()
            if self.name == first_fighter.name: # Guile special power 
                self.special_pow = Guile_Powers
                for pow in self.special_pow: 
                    pow.shoot()

            elif self.name == second_fighter.name: # Ryu special power
                self.special_pow = Ryu_Powers
                for pow in self.special_pow: 
                    pow.shoot()

        if pygame.time.get_ticks() - self.update_time > 600:
            self.update_time = pygame.time.get_ticks()
            self.action = 'idle'
            self.draw()

class Power_Shoot():
    """Create special power object and shooting"""
    def __init__(self, fighter_X, fighter_Y, image, x_vel):
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))
        self.x = fighter_X
        self.y = fighter_Y 
        self.x_vel = x_vel

    def shoot(self):
        self.x += self.x_vel
        screen.blit(self.image, (self.x, self.y))


# game variables

background_img = Background()
first_fighter = Fighter(250, 250, 'Guile', 0.8, power1_sound)
second_fighter = Fighter(950, 250, 'Ryu', 0.7, power2_sound)
move_left = False
move_right = False
run = True
Ryu_Powers = [Power_Shoot( second_fighter.x, second_fighter.y, 'char_img/Ryu/power_1.png', 5),
            Power_Shoot(second_fighter.x, second_fighter.y, 'char_img/Ryu/power_1.png', 10)]
Guile_Powers = [Power_Shoot(first_fighter.x, first_fighter.y, 'char_img/Guile/power_1.png', 1),
            Power_Shoot(first_fighter.x, first_fighter.y, 'char_img/Guile/power_2.png', 5),
            Power_Shoot(first_fighter.x, first_fighter.y, 'char_img/Guile/power_1.png', 10)]


while run:  # the run loop
    punch = False
    kick = False
    special_power = False
    clock.tick(fps)  # set up the same speed of display for any animation in the game

    # draw background
    background_img.update()
    background_img.draw()

    # draw fighters:
    first_fighter.draw()
    # first_fighter.test()
    second_fighter.draw()

    for event in pygame.event.get():
        """Exit game input"""
        if event.type == pygame.QUIT:
            run = False

        """Character left/right movement input/ Hold pressed key"""
        if event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_b:  # input key is B
                move_left = True
            if event.key == pygame.K_f:  # input key is F
                move_right = True
            if event.key == pygame.K_SPACE:
                first_fighter.jump = True
            if event.key == pygame.K_p:  # punch
                first_fighter.action = 'punch'
            if event.key == pygame.K_k:  # kick
                first_fighter.action = 'kick'
            if event.key == pygame.K_s:  # special power
                first_fighter.action = 'special_power'

        if event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_b:  # key B released
                move_left = False
            if event.key == pygame.K_f:  # key F is released
                move_right = False

    if first_fighter.alive:
        first_fighter.move(move_left, move_right)
        first_fighter.attack()
        first_fighter.jumping()

    pygame.display.update()  # to update all added images
pygame.quit()
