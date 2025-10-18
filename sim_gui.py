import pygame 
import curses
import time
'''
Normalizes the given vector.

:param vector: A 2 dimensional vector.
:type vector: ``np.array``
:return: The given vector normalized.
:rtype: ``np.array``
'''

"""
This class encapsulates a pygame window. It renders all activity from the simulation.
"""
class SimGUI():

    def __init__(self):
        pass

    """
    Runs the window.
    """
    def display_sim(self):

        pygame.init()
        self.window_dim = (500, 500)
        self.window = pygame.display.set_mode(self.window_dim)
        self.caption = "Sandevistan!!!"
        pygame.display.set_caption(self.caption)
        self.sim_on = False
        
        self.sim_on = True
        clock = pygame.time.Clock()

        while self.sim_on:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            self.window.fill("black")

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def draw():
        pass


if __name__ == "__main__":
    gui = SimGUI()
    gui.run()
    