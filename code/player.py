import pygame

from entity import Entity 
from screen import Screen
from keylistener import KeyListener
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener : KeyListener, screen : Screen, x: int, y: int):
        super().__init__(keylistener, screen, x , y)
        
        self.pokedollars: int = 0
        
        self.spritesheet_bike: pygame.Surface = pygame.image.load("assets/sprite/hero_01_red_m_cycle_roll.png")
        
        self.switchs: list[Switch] | None = None
        self.collision: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None
        
        
    def update(self) -> None:
        self.check_input()
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:    
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_LEFT):
                temp_hitbox.x -= 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"   
            elif self.keylistener.key_pressed(pygame.K_RIGHT):
                temp_hitbox.x += 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"   
            elif self.keylistener.key_pressed(pygame.K_UP):
                temp_hitbox.y -= 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"        
            elif self.keylistener.key_pressed(pygame.K_DOWN):
                temp_hitbox.y += 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"                
        
    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs
        
    
    def check_collision_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
            return None
        
        
    def add_collision(self, collision):
        self.collision = collision
        
        
    def check_collision(self, temp_hitbox: pygame.Rect):
        if self.collision is None:
            self.collision = []  # Ou gérer l'erreur/initialiser comme nécessaire
        for collision in self.collision:
            if temp_hitbox.colliderect(collision):
                return True
        return False
    
    def check_input(self):
        if self.keylistener.key_pressed(pygame.K_SPACE):
            self.switch_bike()
    
    def switch_bike(self, desactive=False):
        if self.speed == 1 and not desactive:
            self.speed = 3
            self.all_images = self.get_all_images(self.spritesheet_bike)
        else:
            self.speed = 1
            self.all_images = self.get_all_images(self.spritesheet)
        self.keylistener.remove_keys(pygame.K_SPACE)