import pygame
import consts

class GridWindow:
    # initialize the window with the given properties
    def __init__(self, default_p="0.5", default_l="2", default_s1="0.25", default_s2="0.25", default_s3="0.25",
                 default_s4="0.25"):
        pygame.init()
        screen_info = pygame.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h
        min_size = min(self.width, self.height) * 0.9
        self.size = (min_size, min_size)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Rumor Simulation")
        self.done = False
        self.clock = pygame.time.Clock()
        self.input_values = [default_p, default_l, default_s1, default_s2, default_s3, default_s4]
        self.wrap_around = False

    # toggle the wrap around value
    def toggle_wrap_around(self):
        self.wrap_around = not self.wrap_around
    
    # dispaly menu and handle menu events
    def run_menu(self):
        # set up the font for the title
        title_font = pygame.font.SysFont(None, int(55 * min(self.width, self.height) / 1080))
        title_text = title_font.render("Welcome To Rumor Spread Simulator!", True, consts.GREEN)

        starting_x = int(200 * min(self.width, self.height) / 1080)
        starting_y = int(200 * min(self.width, self.height) / 1080)
        input_width = int(200 * min(self.width, self.height) / 1080)
        input_height = int(32 * min(self.width, self.height) / 1080)
        margin = int(50 * min(self.width, self.height) / 1080)

        FONT = pygame.font.Font(None, int(32 * min(self.width, self.height) / 1080))

        input_boxes = [pygame.Rect(starting_x, starting_y + i * margin, input_width, input_height) for i in range(len(self.input_values))]

        wrap_around_check_box = pygame.Rect(starting_x + int(66 * min(self.width, self.height) / 1080), starting_y + len(input_boxes) * margin, int(50 * min(self.width, self.height) / 1080), int(50 * min(self.width, self.height) / 1080))
        start_button = pygame.Rect(starting_x, starting_y + (len(input_boxes) + 2) * margin, int(200 * min(self.width, self.height) / 1080), int(50 * min(self.width, self.height) / 1080))

        labels = [
            FONT.render("P:", True, consts.BLACK),
            FONT.render("L:", True, consts.BLACK),
            FONT.render("S1:", True, consts.BLACK),
            FONT.render("S2:", True, consts.BLACK),
            FONT.render("S3:", True, consts.BLACK),
            FONT.render("S4:", True, consts.BLACK),
            FONT.render("Wrap-Around:", True, consts.BLACK),

        ]
        running = True
        while running:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the start button was clicked
                    if wrap_around_check_box.collidepoint(event.pos):
                        self.toggle_wrap_around()
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

            bg = pygame.Color(consts.BACKGROUND)
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

            if self.wrap_around:
                pygame.draw.rect(self.screen, consts.GREEN, wrap_around_check_box)
            else:
                pygame.draw.rect(self.screen, consts.RED, wrap_around_check_box)

            # Draw title
            self.screen.blit(title_text, (self.size[0] / 2 - title_text.get_width() / 2, 30))

            # Update the display
            pygame.display.flip()

    # handle start button press event
    def handle_start_button(self):
        p = self.input_values[0]
        l = self.input_values[1]
        s1 = self.input_values[2]
        s2 = self.input_values[3]
        s3 = self.input_values[4]
        s4 = self.input_values[5]

        if l.isnumeric() and self.is_float(l) and self.is_float(s1) and self.is_float(s2) and self.is_float(
                s3) and self.is_float(s4):
            p = float(p)
            l = int(l)
            s1 = float(s1)
            s2 = float(s2)
            s3 = float(s3)
            s4 = float(s4)
            if s1 + s2 + s3 + s4 == 1:
                return True, l, p, s1, s2, s3, s4, self.wrap_around
            else:
                error_msg = "Error: The sum of S1, S2, S3, and S4 must equal 1.... Existing...."
                FONT = pygame.font.Font(None, 32)
                text_surface = FONT.render(error_msg, True, consts.RED)
                self.screen.blit(text_surface, (50, 600))
                pygame.display.flip()
        else:
            error_msg = "Error: Invalid input. L must be an integer and P, S1, S2, S3, S4 must be floats..... Existing...."
            FONT = pygame.font.Font(None, 32)
            text_surface = FONT.render(error_msg, True, consts.RED)
            self.screen.blit(text_surface, (50, 600))
            pygame.display.flip()
        return False, l, p, s1, s2, s3, s4, self.wrap_around

    # returns True if the input string is a floating point number
    def is_float(self, string):
        if string.count('.') <= 1 and string.replace(".", "").isnumeric():
            return True
        else:
            return False

    # returns if the window is still running
    def running(self):
        return not self.done

    # draw a simulator round
    def draw(self, grid, colorMode="has_rumor"):
        matrix = grid.get_matrix()
        self.screen.fill(consts.WHITE)
        square_size = self.size[0] / consts.Size
        for i in range(0, consts.Size):
            for j in range(0, consts.Size):
                x1 = i * square_size
                y1 = j * square_size
                if matrix[i][j] is None:
                    pass
                elif colorMode == "has_rumor":
                    if matrix[i][j].get_has_rumor():
                        color = consts.RED
                    else:
                        color = consts.GREEN
                    pygame.draw.rect(self.screen, color, (x1, y1, square_size, square_size), 0)

                # draw by belief level
                elif colorMode == "belief":
                    if matrix[i][j].get_belief() == 1:
                        color = consts.GREEN
                    elif matrix[i][j].get_belief() == 2:
                        color = consts.PINK
                    elif matrix[i][j].get_belief() == 3:
                        color = consts.RED
                    elif matrix[i][j].get_belief() == 4:
                        color = consts.BLACK
                    pygame.draw.rect(self.screen, color, (x1, y1, square_size, square_size), 0)

        pygame.display.flip()
        self.clock.tick(60)

    # if quit event accur, quit the game
    def check_if_done(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    # exit game
    def exit(self):
        pygame.quit()