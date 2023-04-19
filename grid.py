import consts
import numpy as np
from person import Person
from collections import deque


class Grid:
    # initialize the grid with the given parameters
    def __init__(self, l, p, s1_precent, s2_precent, s3_precent, s4_precent, wrap_around, mode='random'):
        self.matrix = [[None for _ in range(consts.Size)] for _ in range(consts.Size)]
        self.l = l
        self.p = p
        self.grid_size = consts.Size * consts.Size
        self.same_state_counter = 0
        self.state = None
        self.wrap_around = wrap_around

        s1_number = int(p * self.grid_size * s1_precent)
        s2_number = int(p * self.grid_size * s2_precent)
        s3_number = int(p * self.grid_size * s3_precent)
        s4_number = int(p * self.grid_size * s4_precent)

        if mode == 'random':
            chosen_location = self.init_at_random_locations(s1_number, s2_number, s3_number, s4_number)
        if mode == 'slowSpread':
            chosen_location = self.init_slow_spread_blocks(s1_number, s2_number, s3_number, s4_number)
        if mode == 'fastSpread':
            chosen_location = self.init_fast_spread(s1_number, s2_number, s3_number, s4_number)

        self.matrix[chosen_location[0]][chosen_location[1]].set_belive_rumor()
        self.first_person = self.matrix[chosen_location[0]][chosen_location[1]]
        self.has_rumor_list = {self.first_person}
        self.current_rumor_exposed = {self.first_person}

    # set the grid matrix with people in random locations.
    # return the locations and a random location form them.
    def generate_persons_at_random_locations(self):
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]
            self.matrix[row_idx][col_idx] = Person(2, [row_idx, col_idx], consts.Size, consts.Size)

        return random_indices, chosen_location

    # assign beliefs to the unassigned people by s_numbers priority order
    def assign_beliefs_by_order(self, indices, assigned_people, s_numbers):
        for idx in indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            current = self.matrix[row_idx][col_idx]
            if current and current not in assigned_people:
                for i, s_num in enumerate(s_numbers):
                    if s_num > 0:
                        person_belief = i + 1
                        s_numbers[i] -= 1
                        current.set_belief(person_belief)
                        break

    # assign beliefs to the unassigned people by blocks order
    def assign_beliefs_by_blocks(self, row_start, row_end, col_start, col_end, assigned_people, s_numbers, beliefs):
        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                current = self.matrix[row][col]
                if current:
                    for index, (s_num, belief) in enumerate(zip(s_numbers, beliefs)):
                        if s_num > 0:
                            s_numbers[index] -= 1
                            assigned_people.append(current)
                            current.set_belief(belief)
                            break
        return s_numbers

    # init the grid with people in random locations,
    # assigns random beliefs and return startig rumor location.
    def init_at_random_locations(self, s1_number, s2_number, s3_number, s4_number):
        random_indices, chosen_location = self.generate_persons_at_random_locations()
        s_numbers = [s1_number, s2_number, s3_number, s4_number]
        self.assign_beliefs_by_order(random_indices, [], s_numbers)
        return chosen_location

    # init the grid with people in blocks shaped style,
    # assigns beliefs to each block and return startig rumor location.
    def init_slow_spread_blocks(self, s1_number, s2_number, s3_number, s4_number):
        random_indices, chosen_location = self.generate_persons_at_random_locations()
        middle = int(consts.Size / 2)
        assigned_people = []
        s1_number, s4_number = self.assign_beliefs_by_blocks(0, middle, 0, middle, assigned_people,
                                                             [s1_number, s4_number], [1, 4])
        s3_number = \
        self.assign_beliefs_by_blocks(middle, consts.Size, middle, consts.Size, assigned_people, [s3_number], [3])[0]
        s4_number = self.assign_beliefs_by_blocks(0, middle, middle, consts.Size, assigned_people, [s4_number], [4])[0]
        s4_number, s2_number = self.assign_beliefs_by_blocks(middle, consts.Size, 0, middle, assigned_people,
                                                             [s4_number, s2_number], [4, 2])
        s_numbers = [s1_number, s2_number, s3_number, s4_number]
        self.assign_beliefs_by_order(random_indices, assigned_people, s_numbers)
        return chosen_location

    # init the grid where all s1 people in corner blocks and the rest are in the middle.
    # returns the starting rumor location.
    def init_slow_spread(self, s1_number, s2_number, s3_number, s4_number):
        random_indices, chosen_location = self.generate_persons_at_random_locations()
        s_numbers = [s1_number, s2_number, s3_number, s4_number]
        corner_order = deque([])

        for corner_num, s_num in [(1, s1_number), (2, s2_number), (1, s1_number), (4, s4_number)]:
            if s_num > 1:
                corner_order.append(corner_num)
                corner_order.append(corner_num)

        limit = consts.Size - 1
        square_size = 40
        assigned_people = []
        for col in range(square_size):
            squares_people, squares_edge_people = self.get_square_people(col, square_size, limit)
            for person in squares_people:
                if not corner_order:
                    break
                assigned_people.append(person)
                belief = corner_order[0]
                person.set_belief(belief)
                s_number_idx = belief - 1
                s_numbers[s_number_idx] -= 1

                if s_numbers[s_number_idx] <= 0:
                    while belief in corner_order:
                        corner_order.remove(belief)
                else:
                    corner_order.rotate(-1)

        for person in squares_edge_people:
            belief = 4
            s_number_idx = belief - 1
            if s_numbers[s_number_idx] > 0:
                assigned_people.append(person)
                person.set_belief(belief)
                s_numbers[s_number_idx] -= 1

        self.assign_beliefs_by_order(random_indices, assigned_people, s_numbers)
        return chosen_location

    # init the grid with people in random locations and assign beliefs in round roubin order
    # on the grid's rows.
    # returns the starting rumor location.
    def init_fast_spread(self, s1_number, s2_number, s3_number, s4_number):
        random_indices, chosen_location = self.generate_persons_at_random_locations()

        round = deque([])

        for corner_num, s_num in [(1, s1_number), (2, s2_number), (3, s1_number), (4, s4_number)]:
            if s_num > 1:
                round.append(corner_num)
        belief_counts = {1: s1_number, 2: s2_number, 3: s3_number, 4: s4_number}

        for row in range(consts.Size):
            for col in range(consts.Size):
                if self.matrix[row][col] is not None:
                    belief_num = round[0]
                    self.matrix[row][col].set_belief(belief_num)
                    if belief_num in belief_counts:
                        belief_counts[belief_num] -= 1
                        if belief_counts[belief_num] == 0:
                            round.popleft()
                        if len(round) == 0:
                            break
                    round.rotate(-1)
        return chosen_location

    # init the grid with people in random locations and assign beliefs in round roubin order on the
    # grid's diagonals.
    def init_fast_spread_diagonal(self, s1_number, s2_number, s3_number, s4_number):
        random_indices, chosen_location = self.generate_persons_at_random_locations()

        s_numbers = [s1_number, s2_number, s3_number, s4_number]
        round_order = deque([])

        for corner_num, s_num in [(1, s1_number), (2, s2_number), (3, s1_number), (4, s4_number)]:
            if s_num > 1:
                round_order.append(corner_num)

        for i in range(consts.Size):
            if not round_order:
                break
            # Traverse the diagonal and the reverse diagonal at index i
            diagonal = [self.matrix[j][j + i] for j in range(consts.Size - i) if self.matrix[j][j + i]]
            diagonal_reverse = [self.matrix[j + i][j] for j in range(consts.Size - i) if self.matrix[j + i][j]]
            for person in diagonal + diagonal_reverse:
                if not round_order:
                    break

                belief = round_order[0]
                person.set_belief(belief)

                s_number_idx = belief - 1
                s_numbers[s_number_idx] -= 1

                if s_numbers[s_number_idx] <= 0:
                    while belief in round_order:
                        round_order.remove(belief)
                else:
                    round_order.rotate(-1)
        return chosen_location

    # runs a round of rumor spread in the grid
    def run(self):
        current_round_rumor_set = set()

        for person in self.has_rumor_list:
            believers_to_rumor, exposed_to_rumor = person.spread_rumor(self.matrix, self.l, self.wrap_around)
            current_round_rumor_set.update(believers_to_rumor)
            self.current_rumor_exposed = self.current_rumor_exposed.union(exposed_to_rumor)

        self.state = self.has_rumor_list
        self.has_rumor_list = self.has_rumor_list.union(current_round_rumor_set)

        for i in range(0, consts.Size):
            for j in range(0, consts.Size):
                if self.matrix[i][j] != None:
                    self.matrix[i][j].reset_belief()
                    if self.matrix[i][j].is_waiting():
                        self.matrix[i][j].wait_round()
        return True

    # getter for the grid matrix
    def get_matrix(self):
        return self.matrix

    # returns the precentage of people the has the rumor
    def has_rumor_precentage(self):
        return (len(self.has_rumor_list) / (self.p * self.grid_size)) * 100

    # returns the precentage of people the has been exposed to the rumor
    def exposed_rumor_precentage(self):
        return (len(self.current_rumor_exposed) / (self.p * self.grid_size)) * 100

    # returns list of people which are inside the square and list of people which are on the square edge.
    def get_square_people(self, col, square_size, limit):
        top_left_corner = [self.matrix[row][col] for row in range(square_size) if self.matrix[row][col]]

        top_left_edge = [self.matrix[row][col] for row in range(square_size, square_size + 1) if
                         self.matrix[row][col]] + \
                        [self.matrix[row][col + 1] for row in range(square_size) if self.matrix[row][col + 1]]

        bottom_left_corner = [self.matrix[row][limit - col] for row in range(square_size) if
                              self.matrix[row][limit - col]]

        bottom_left_edge = [self.matrix[row][limit - col] for row in range(square_size, square_size + 1) if
                            self.matrix[row][limit - col]] + \
                           [self.matrix[row][limit - col - 1] for row in range(square_size) if
                            self.matrix[row][limit - col - 1]]

        bottom_right_corner = [self.matrix[limit - row][limit - col] for row in range(square_size) if
                               self.matrix[limit - row][limit - col]]

        bottom_right_edge = [self.matrix[limit - row][limit - col] for row in range(square_size, square_size + 1)
                             if self.matrix[limit - row][limit - col]] + \
                            [self.matrix[limit - row][limit - col - 1] for row in range(square_size) if
                             self.matrix[limit - row][limit - col - 1]]

        top_right_corner = [self.matrix[limit - row][col] for row in range(square_size) if
                            self.matrix[limit - row][col]]

        top_right_edge = [self.matrix[limit - row][col] for row in range(square_size, square_size + 1) if
                          self.matrix[limit - row][col]] + \
                         [self.matrix[limit - row][col + 1] for row in range(square_size) if
                          self.matrix[limit - row][col + 1]]

        squares_people = top_left_corner + bottom_left_corner + bottom_right_corner + top_right_corner
        squares_edge_people = top_left_edge + bottom_left_edge + bottom_right_edge + top_right_edge

        return squares_people, squares_edge_people