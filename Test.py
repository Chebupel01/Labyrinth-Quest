import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from random import randint
import pygame


class PlanetLandscape:
    def __init__(self):
        noise = PerlinNoise(octaves=24)
        noise2 = PerlinNoise(octaves=32)
        noise3 = PerlinNoise(octaves=2)
        noise4 = PerlinNoise(octaves=8)
        landscape = []
        terrarian_scale = 300
        for x in range(terrarian_scale):
            row = []
            for y in range(terrarian_scale):
                noise_val = noise([x / terrarian_scale, y / terrarian_scale])
                noise_val += 0.5 * noise2([x / terrarian_scale, y / terrarian_scale])
                noise_val += 0.25 * noise3([x / terrarian_scale, y / terrarian_scale])
                noise_val += 0.125 * noise4([x / terrarian_scale, y / terrarian_scale])
                row.append(noise_val)
            landscape.append(row)
        self.landscape = np.array(landscape)
        print(landscape)

    def render(self, screen, playercords):
        LandscapeForRendering = self.landscape[playercords[0]:playercords[0] + 100, playercords[1]:playercords[1] + 50]
        x1 = 0
        for x in range(playercords[0], playercords[0] + len(LandscapeForRendering)):
            y1 = 0
            for y in range(playercords[1], playercords[1] + len(LandscapeForRendering[0])):
                if self.landscape[x][y] >= 0.2:
                    if self.landscape[x][y] <= 0.25:
                        pygame.draw.rect(screen, (244, 164, 96), (x1, y1, 16, 16))
                    if self.landscape[x][y] <= 0.33:
                        pygame.draw.rect(screen, (63, 94, 179), (x1, y1, 16, 16))
                    else:
                        pygame.draw.rect(screen, (81, 114, 175), (x1, y1, 16, 16))
                else:
                    """if self.landscape[x][y] <= 0.7:
                        pygame.draw.rect(screen, (255, 250, 250), (x * 16, y * 16, 16, 16))
                    else:"""
                    pygame.draw.rect(screen, (0, 158, 0), (x1, y1, 16, 16))
                y1 += 16
            x1 += 16
        return screen


class Player:
    def __init__(self):
        self.cords = [0, 0]

    def renderPlayer(self, screen, cords):
        pygame.draw.rect(screen, 'red', (cords[0], cords[1], 30, 55))


if __name__ == '__main__':
    planet = PlanetLandscape()
    running = True
    screen = pygame.display.set_mode([1600, 800])
    player = Player()
    playercords = [0, 0]
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                playercords[0], playercords[1] = playercords[0], playercords[1] - 1
            elif keys[pygame.K_s]:
                playercords[0], playercords[1] = playercords[0], playercords[1] + 1
            elif keys[pygame.K_a]:
                playercords[0], playercords[1] = playercords[0] - 1, playercords[1]
            elif keys[pygame.K_d]:
                playercords[0], playercords[1] = playercords[0] + 1, playercords[1]
        screen = planet.render(screen, playercords)
        player.renderPlayer(screen, playercords)
        pygame.display.flip()
        clock.tick(60)