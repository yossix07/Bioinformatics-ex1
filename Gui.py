import pygame
import consts


class GridWindow:
    def __init__(self):
        pygame.init()
        FONT = pygame.font.Font(None, 32)
        input_boxes = [
        pygame.Rect(200, 200, 200, 32),  # P
        pygame.Rect(200, 250, 200, 32),  # L
        pygame.Rect(200, 300, 200, 32),  # S1
        pygame.Rect(200, 350, 200, 32),  # S2
        pygame.Rect(200, 400, 200, 32),  # S3
        pygame.Rect(200, 450, 200, 32),  # S4
        ]

        # Define the default input values
        input_values = ["", "", "", "", "", ""]

        # Define the start button
        start_button = pygame.Rect(200, 500, 200, 50)

    # Define the text labels
        labels = [
        FONT.render("P:", True, consts.BLACK),
        FONT.render("L:", True, consts.BLACK),
        FONT.render("S1:", True, consts.BLACK),
        FONT.render("S2:", True, consts.BLACK),
        FONT.render("S3:", True, consts.BLACK),
        FONT.render("S4:", True, consts.BLACK),
        FONT.render("Start", True, consts.BLACK),
        ]

        self.size = (1000, 1000)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Rumor Simulation")
        self.done = False
        self.clock = pygame.time.Clock()

    def running(self):
        return not self.done

    def draw(self, grid, colorMode="has_rumor"):
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
                elif colorMode == "has_rumor":
                    if matrix[i][j].get_has_rumor():
                        #counter += 1
                        pygame.draw.rect(self.screen, consts.RED, (x1, y1, square_size, square_size), 0)
                    else:
                        pygame.draw.rect(self.screen, consts.GREEN, (x1, y1, square_size, square_size), 0)

                # draw by belief level
                elif colorMode == "belief":
                    if matrix[i][j].get_belief() == 1:
                        pygame.draw.rect(self.screen, consts.RED, (x1, y1, square_size, square_size), 0)
                    elif matrix[i][j].get_belief() == 2:
                        pygame.draw.rect(self.screen, consts.GREEN, (x1, y1, square_size, square_size), 0)
                    elif matrix[i][j].get_belief() == 3:
                        pygame.draw.rect(self.screen, consts.BLACK, (x1, y1, square_size, square_size), 0)
                    elif matrix[i][j].get_belief() == 4:
                        pygame.draw.rect(self.screen, consts.PINK, (x1, y1, square_size, square_size), 0)

        #print(counter)
        pygame.display.flip()
        self.clock.tick(60)

    def check_if_done(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def exit(self):
        pygame.quit()