import os

import pygame


class ImageControler:
    def __init__(self, WIDTH: float, HEIGHT: float):
        # load images
        self.background_images = {}
        self.pokImages = {}
        self.agentsImages = {}
        b0 = pygame.image.load(os.path.join('../pics_for_game', 'background.jpg'))
        b0 = pygame.transform.scale(b0, (WIDTH, HEIGHT))
        self.background_images[0] = b0

        pikacuIM = pygame.image.load(os.path.join('../pics_for_game', 'pikachu.jpg'))
        pikacuIM = pygame.transform.scale(pikacuIM, (50, 50))
        self.pokImages[0] = pikacuIM

        koffingIM = pygame.image.load(os.path.join('../pics_for_game', 'koffing.jpg'))
        koffingIM = pygame.transform.scale(koffingIM, (50, 50))
        self.pokImages[1] = koffingIM

        psyduckIM = pygame.image.load(os.path.join('../pics_for_game', 'psyduck.jpg'))
        psyduckIM = pygame.transform.scale(psyduckIM, (50, 50))
        self.pokImages[2] = psyduckIM

        squirtleIM = pygame.image.load(os.path.join('../pics_for_game', 'squirtle.jpg'))
        squirtleIM = pygame.transform.scale(squirtleIM, (50, 50))
        self.pokImages[3] = squirtleIM

        jigglupuffIM = pygame.image.load(os.path.join('../pics_for_game', 'jigglupuff.jpg'))
        jigglupuffIM = pygame.transform.scale(jigglupuffIM, (50, 50))
        self.pokImages[4] = jigglupuffIM

        alakazamIM = pygame.image.load(os.path.join('../pics_for_game', 'alakazam.jpg'))
        alakazamIM = pygame.transform.scale(alakazamIM, (50, 50))
        self.pokImages[5] = alakazamIM

        bulbasaurIM = pygame.image.load(os.path.join('../pics_for_game', 'bulbasaur.jpg'))
        bulbasaurIM = pygame.transform.scale(bulbasaurIM, (50, 50))
        self.pokImages[6] = bulbasaurIM

        charizardIM = pygame.image.load(os.path.join('../pics_for_game', 'charizard.jpg'))
        charizardIM = pygame.transform.scale(charizardIM, (50, 50))
        self.pokImages[7] = charizardIM

        rattataIM = pygame.image.load(os.path.join('../pics_for_game', 'rattata.jpg'))
        rattataIM = pygame.transform.scale(rattataIM, (50, 50))
        self.pokImages[8] = rattataIM

        kyorgeIM = pygame.image.load(os.path.join('../pics_for_game', 'kyorge.jpg'))
        kyorgeIM = pygame.transform.scale(kyorgeIM, (50, 50))
        self.pokImages[9] = kyorgeIM

        mewtwoIM = pygame.image.load(os.path.join('../pics_for_game', 'mewtwo.jpg'))
        mewtwoIM = pygame.transform.scale(mewtwoIM, (50, 50))
        self.pokImages[10] = mewtwoIM

        ashIM = pygame.image.load(os.path.join('../pics_for_game', 'ash.jpg'))
        ashIM = pygame.transform.scale(ashIM, (30, 60))
        self.agentsImages[0] = ashIM

        brookIM = pygame.image.load(os.path.join('../pics_for_game', 'brook.jpg'))
        brookIM = pygame.transform.scale(brookIM, (40, 80))
        self.agentsImages[1] = brookIM

        mistyIM = pygame.image.load(os.path.join('../pics_for_game', 'misty.jpg'))
        mistyIM = pygame.transform.scale(mistyIM, (40, 80))
        self.agentsImages[2] = mistyIM
