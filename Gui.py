import pygame
import consts


class GridWindow:
    def __init__(self):
        pygame.init()
        self.size = (1000, 1000)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("My Game")
        self.done = False
        self.clock = pygame.time.Clock()

    def running(self):
        return not self.done

    def draw(self, grid):
        matrix = grid.get_matrix()
        self.screen.fill(consts.WHITE)
        square_size = 10
        #counter=0
        for i in range(0, consts.Size):
            for j in range(0, consts.Size):
                x1 = i * square_size
                y1 = j * square_size
                if matrix[i][j] is None:
                    pygame.draw.rect(self.screen, consts.WHITE, (x1, y1, square_size, square_size), 0)
                # else:
                #     if matrix[i][j].get_has_rumor():
                #         #counter += 1
                #         pygame.draw.rect(self.screen, consts.RED, (x1, y1, square_size, square_size), 0)
                #     else:
                #         pygame.draw.rect(self.screen, consts.GREEN, (x1, y1, square_size, square_size), 0)

                # draw by belief level
                else:
                    if matrix[i][j].get_belief() == 1:
                        #counter += 1
                        pygame.draw.rect(self.screen, consts.RED, (x1, y1, square_size, square_size), 0)
                    elif matrix[i][j].get_belief() == 2:
                        pygame.draw.rect(self.screen, consts.GREEN, (x1, y1, square_size, square_size), 0)
                    elif matrix[i][j].get_belief() == 3:
                        pygame.draw.rect(self.screen, consts.BLACK, (x1, y1, square_size, square_size), 0)
                    elif matrix[i][j].get_belief() == 4:
                        pygame.draw.rect(self.screen, consts.R, (x1, y1, square_size, square_size), 0)

        #print(counter)
        pygame.display.flip()
        self.clock.tick(60)

    def check_if_done(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def exit(self):
        pygame.quit()