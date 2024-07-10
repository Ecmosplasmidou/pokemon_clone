import pygame
from screen import Screen
from map import Map
from entity import Entity
from keylistener import KeyListener
from player import Player
from controller import Controller
from option import Option
from save import Save

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = Screen()
        self.controller = Controller()
        self.map = Map(self.screen, self.controller)
        self.keylistener = KeyListener()   
        self.player = Player(self.controller, self.screen, self.keylistener, 255, 207)
        self.map.add_player(self.player)
        self.save = Save("save_0", self.map)
        self.option = Option(self.screen, self.controller, self.map, "fr", self.save, self.keylistener)
                
        
    def run(self):
        while self.running:
            self.handle_input()
            if not self.player.menu_option:
                self.map.update()
            else:
                self.option.update()
            self.map.update()
            self.screen.update()
            
            
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_keys(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_keys(event.key)