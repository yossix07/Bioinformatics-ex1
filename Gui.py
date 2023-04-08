import pygame
import consts

class GridWindow:
    def __init__(self, default_p="0.5", default_l="2", default_s1="0.25", default_s2="0.25", default_s3="0.25", default_s4="0.25"):
        pygame.init()
        self.size = (1000, 1000)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Rumor Simulation")
        self.done = False
        self.clock = pygame.time.Clock()
        # Define the default input values
        self.input_values = [default_p, default_l, default_s1, default_s2, default_s3, default_s4]

    def run_menu(self):
        
        # set up the font for the title
        title_font = pygame.font.SysFont(None, 55)
        title_text = title_font.render("Welcome To Rumor Spread Simulator!", True, consts.GREEN)

        FONT = pygame.font.Font(None, 32)
        input_boxes = [
        pygame.Rect(200, 200, 200, 32),  # P
        pygame.Rect(200, 250, 200, 32),  # L
        pygame.Rect(200, 300, 200, 32),  # S1
        pygame.Rect(200, 350, 200, 32),  # S2
        pygame.Rect(200, 400, 200, 32),  # S3
        pygame.Rect(200, 450, 200, 32),  # S4
        ]

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
        
        ]
        running = True
        while running:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the start button was clicked
                    if start_button.collidepoint(event.pos):
                        return self.handle_start_button()
                        
                elif event.type == pygame.KEYDOWN:
                    # Check if a key was pressed while an input box was selected
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_BACKSPACE:
                                self.input_values[i] = self.input_values[i][:-1]
                            else:
                                self.input_values[i] += event.unicode

            # Clear the screen
            # self.screen.fill(consts.WHITE)
            bg = pygame.Color((33, 182, 168))
            self.screen.fill(bg)

            # Draw the input boxes
            for i, box in enumerate(input_boxes):
                pygame.draw.rect(self.screen, consts.BLACK, box, 2)
                text_surface = FONT.render(self.input_values[i], True, consts.BLACK)
                self.screen.blit(text_surface, (box.x + 5, box.y + 5))

            # Draw the labels
            for i, label in enumerate(labels):
                self.screen.blit(label, (100, 200 + 50 * i))

            # Draw the start button
            pygame.draw.rect(self.screen, consts.GREEN, start_button)
            self.screen.blit(FONT.render("Start", True, consts.BLACK), (start_button.x + 70, start_button.y + 15))
            
            # Draw title
            self.screen.blit(title_text, (self.size[0]/2 - title_text.get_width()/2, 30))

            # Update the display
            pygame.display.flip()

    def handle_start_button(self):
        p = self.input_values[0]
        l = self.input_values[1]
        s1 = self.input_values[2]
        s2 = self.input_values[3]
        s3 = self.input_values[4]
        s4 = self.input_values[5]

        if l.isnumeric() and self.is_float(l) and self.is_float(s1) and self.is_float(s2) and self.is_float(s3) and self.is_float(s4):
            p = float(p)
            l = int(l)
            s1 = float(s1)
            s2 = float(s2)
            s3 = float(s3)
            s4 = float(s4)
            if s1 + s2 + s3 + s4 == 1:
                return True, l, p, s1, s2, s3, s4
            else:
                error_msg = "Error: The sum of S1, S2, S3, and S4 must equal 1"
                FONT = pygame.font.Font(None, 32)
                text_surface = FONT.render(error_msg, True, consts.BLACK)
                self.screen.blit(text_surface, (240, 550))
        else:
            error_msg = "Error: Invalid input. L must be an integer and P, S1, S2, S3, S4 must be floats."
            FONT = pygame.font.Font(None, 32)
            text_surface = FONT.render(error_msg, True, consts.BLACK)
            self.screen.blit(text_surface, (240, 550))
        print(error_msg)
        return False, l, p, s1, s2, s3, s4
    

    def is_float(self, string):
        if string.count('.') <= 1 and string.replace(".", "").isnumeric():
            return True
        else:
            return False

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