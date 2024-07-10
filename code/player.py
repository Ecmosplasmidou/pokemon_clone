import pygame
import datetime

from entity import Entity 
from screen import Screen
from switch import Switch
from pokemon import Pokemon
from controller import Controller
from keylistener import KeyListener


class Player(Entity):
    def __init__(self, screen : Screen, controller: Controller, keylistenner: KeyListener, x: int, y: int, ingame_time = datetime.timedelta(seconds=0)):
        super().__init__(screen, x , y)
        
        self.name = "Red"
        self.keylistener = keylistenner
        self.controller = Controller()
        self.screen = Screen()
        self.pokedollars = 0
        self.pokemons = []
        self.pokemons.append(Pokemon.createPokemon("Charmander", 5))
        self.inventory = None
        self.pokedex = None
        self.ingame_time: datetime.timedelta = ingame_time
        
        
        self.spritesheet_bike: pygame.Surface = pygame.image.load("assets/sprite/hero_01_red_m_cycle_roll.png")
        
        self.menu_option: bool = False
        
        self.switchs: list[Switch] | None = None
        self.collision: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None
        
        
    def update(self) -> None:
        self.update_ingame_time()
        self.check_input()
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:    
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(self.controller.get_key("left")):
                temp_hitbox.x -= 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_left()
                    print("Mouvement vers la gauche")
                else:
                    self.direction = "left"   
            elif self.keylistener.key_pressed(self.controller.get_key("right")):
                temp_hitbox.x += 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_right()
                    print("Mouvement vers la droite")
                else:
                    self.direction = "right"   
            elif self.keylistener.key_pressed(self.controller.get_key("up")):
                temp_hitbox.y -= 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_up()
                    print("Mouvement vers le haut")
                else:
                    self.direction = "up"        
            elif self.keylistener.key_pressed(self.controller.get_key("down")):
                temp_hitbox.y += 16
                if not self.check_collision(temp_hitbox):
                    self.check_collision_switchs(temp_hitbox)
                    self.move_down()
                    print("Mouvement vers la bas")
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
        if self.keylistener.key_pressed(self.controller.get_key("bike")):
            self.switch_bike()
        if self.keylistener.key_pressed(self.controller.get_key("escape")):
            self.menu_option = True
            self.keylistener.remove_keys(self.controller.get_key("bike"))
            return
    
    def switch_bike(self, desactive=False):
        if self.speed == 1 and not desactive:
            self.speed = 3
            self.all_images = self.get_all_images(self.spritesheet_bike)
        else:
            self.speed = 1
            self.all_images = self.get_all_images(self.spritesheet)
        self.keylistener.remove_keys(self.controller.get_key("bike"))
        
    def update_ingame_time(self):
        if self.screen.get_delta_time() > 0:
            self.ingame_time += datetime.timedelta(seconds=self.screen.get_delta_time()/10000)
            