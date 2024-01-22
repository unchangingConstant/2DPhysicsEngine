import pygame
from allEntities import *
import collisionHandler as ch
import colorGradient as cg

pygame.init()
windowDim = (500, 500)

win = pygame.display.set_mode(windowDim)
pygame.display.set_caption("Sandevistan!!!")

player = david

allEntities = [david]
environment = [bound1, bound2, bound3, bound4]

run = True

while run:

    print(david.getVelocity())
    win.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    userInput = pygame.key.get_pressed()

    if userInput[pygame.K_a]:
        player.modVelocity(Player.LEFT)
    if userInput[pygame.K_d]:
        player.modVelocity(Player.RIGHT)
    if userInput[pygame.K_w]:
        player.modVelocity(Player.UP)
    if userInput[pygame.K_s]:
        player.modVelocity(Player.DOWN)

    for entity in allEntities:
        ch.resolveMotion(entity, environment)
    
    for entity in allEntities:
        pygame.draw.circle(win, cg.WHITE, entity.getPosition(), 15)

    for surface in environment:
        pygame.draw.line(win, cg.HOT_PINK, surface.edge1, surface.edge2, 3)

    pygame.time.delay(32)

    pygame.display.update()