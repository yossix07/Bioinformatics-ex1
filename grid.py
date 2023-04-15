from random import randint
import consts
import numpy as np
from person import Person
from collections import deque


class Grid:
    def __init__(self, l, p, s1_precent, s2_precent, s3_precent, s4_precent,wrap_around, mode='random'):
        self.matrix = [[None for _ in range(consts.Size)] for _ in range(consts.Size)]
        self.l = l
        self.p = p
        self.current_rumor_exposed = set()
        self.grid_size = consts.Size * consts.Size
        self.same_state_counter = 0
        self.state = None
        self.wrap_around = wrap_around


        s1_number = int(p * self.grid_size * s1_precent)
        s2_number = int(p * self.grid_size * s2_precent)
        s3_number = int(p * self.grid_size * s3_precent)
        s4_number = int(p * self.grid_size * s4_precent)

        print(s1_number, s2_number, s3_number, s4_number)

        if mode == 'random':
            chosen_location = self.init_at_random_locations(s1_number, s2_number, s3_number, s4_number)
        if mode == 'slowSpread':
            chosen_location = self.init_slow_spread(s1_number, s2_number, s3_number, s4_number)
        if mode == 'fastSpread':
            chosen_location = self.init_fast_spread_diagonal(s1_number, s2_number, s3_number, s4_number)

        self.matrix[chosen_location[0]][chosen_location[1]].set_belive_rumor()
        self.first_person = self.matrix[chosen_location[0]][chosen_location[1]]
        self.has_rumor_list = {self.first_person}
        self.current_rumor_exposed = {self.first_person}

    def init_at_random_locations(self, s1_number, s2_number, s3_number, s4_number):
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)
        s_numbers = [s1_number, s2_number, s3_number, s4_number]
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]

            person_belief = 4
            for i, s_num in enumerate(s_numbers):
                if s_num > 0:
                    person_belief = i + 1
                    s_numbers[i] -= 1
                    break
            self.matrix[row_idx][col_idx] = Person(person_belief, [row_idx, col_idx], consts.Size, consts.Size)
        return chosen_location

    def init_slow_spread(self, s1_number, s2_number, s3_number, s4_number):
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]

            self.matrix[row_idx][col_idx] = Person(1, [row_idx, col_idx], consts.Size, consts.Size)

        s_numbers = [s1_number, s2_number, s3_number, s4_number]

        corner_order = deque([])

        if s1_number > 0:
            corner_order.append(1)
            corner_order.append(1)

        if s2_number > 0:
            corner_order.append(2)
            corner_order.append(2)

        if s3_number > 0:
            corner_order.append(3)
            corner_order.append(3)

        if s4_number > 0:
            corner_order.append(4)
            corner_order.append(4)
            corner_order.append(4)

        limit = consts.Size - 1
        border_limit = int(consts.Size / 3)
        assigned_people = []
        for col in range(border_limit):
            top_left_corner = [self.matrix[row][col] for row in range(border_limit) if self.matrix[row][col]]
            top_left_edge = [self.matrix[row][col] for row in range(border_limit, border_limit + 1) if
                             self.matrix[row][col]] + \
                            [self.matrix[row][col + 1] for row in range(border_limit) if self.matrix[row][col + 1]]

            bottom_left_corner = [self.matrix[row][limit - col] for row in range(border_limit) if
                                  self.matrix[row][limit - col]]
            bottom_left_edge = [self.matrix[row][limit - col] for row in range(border_limit, border_limit + 1) if
                                self.matrix[row][limit - col]] + \
                               [self.matrix[row][limit - col - 1] for row in range(border_limit) if
                                self.matrix[row][limit - col - 1]]

            bottom_right_corner = [self.matrix[limit - row][limit - col] for row in range(border_limit) if
                                   self.matrix[limit - row][limit - col]]
            bottom_right_edge = [self.matrix[limit - row][limit - col] for row in range(border_limit, border_limit + 1)
                                 if self.matrix[limit - row][limit - col]] + \
                                [self.matrix[limit - row][limit - col - 1] for row in range(border_limit) if
                                 self.matrix[limit - row][limit - col - 1]]

            top_right_corner = [self.matrix[limit - row][col] for row in range(border_limit) if
                                self.matrix[limit - row][col]]
            top_right_edge = [self.matrix[limit - row][col] for row in range(border_limit, border_limit + 1) if
                              self.matrix[limit - row][col]] + \
                             [self.matrix[limit - row][col + 1] for row in range(border_limit) if
                              self.matrix[limit - row][col + 1]]

            squares_people = top_left_corner + bottom_left_corner + bottom_right_corner + top_right_corner
            squares_edge_people = top_left_edge + bottom_left_edge + bottom_right_edge + top_right_edge
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

        print(s_numbers)
        counter = 0
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            current = self.matrix[row_idx][col_idx]
            if current and current not in assigned_people:
                counter += 1
                for i, s_num in enumerate(s_numbers):
                    if s_num > 0:
                        person_belief = i + 1
                        s_numbers[i] -= 1
                        current.set_belief(person_belief)
                        break
        print(counter)
        # round_order = deque([])

        # if s1_number > 0:
        #     round_order.append(1)
        # if s2_number > 0:
        #     round_order.append(2)
        # if s3_number > 0:
        #     round_order.append(3)
        # if s4_number > 0:
        #     round_order.append(4)
        #     round_order.append(4)

        # for row in range(consts.Size):
        #     for col in range(consts.Size):
        #         current = self.matrix[row][col]
        #         if current and current not in assigned_people:
        #             if not round_order:
        #                 break
        #             belief = round_order[0]
        #             current.set_belief(belief)

        #             s_number_idx = belief - 1
        #             s_numbers[s_number_idx] -= 1

        #             if s_numbers[s_number_idx] <= 0:
        #                 while belief in round_order:
        #                     round_order.remove(belief)
        #             else:
        #                 round_order.rotate(-1)

        # print(s_numbers)
        return chosen_location

    def init_fast_spread(self, s1_number, s2_number, s3_number, s4_number):
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]

            self.matrix[row_idx][col_idx] = Person(2, [row_idx, col_idx], consts.Size, consts.Size)

        round = deque([])

        if s1_number > 0:
            round.append(1)
        if s2_number > 0:
            round.append(2)
        if s3_number > 0:
            round.append(3)
        if s4_number > 0:
            round.append(4)

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

    def init_fast_spread_diagonal(self, s1_number, s2_number, s3_number, s4_number):
        # Choose random indices for the initial infected people
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)
        chosen_location = None

        s_numbers = [s1_number, s2_number, s3_number, s4_number]

        # Create a Person object at each index and assign them to the matrix
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            self.matrix[row_idx][col_idx] = Person(4, [row_idx, col_idx], consts.Size, consts.Size)

            if idx == random_location:
                chosen_location = [row_idx, col_idx]

        round_order = deque([])

        if s1_number > 0:
            round_order.append(1)

        if s2_number > 0:
            round_order.append(2)

        if s3_number > 0:
            round_order.append(3)

        if s4_number > 0:
            round_order.append(4)

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

    def run(self):
        current_round_rumor_set = set()

        for person in self.has_rumor_list:
            believers_to_rumor, exposed_to_rumor = person.spread_rumor(self.matrix, self.l,self.wrap_around)
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

    def get_matrix(self):
        return self.matrix

    def has_rumor_precentage(self):
        return (len(self.has_rumor_list) / (self.p * self.grid_size)) * 100

    def exposed_rumor_precentage(self):
        return (len(self.current_rumor_exposed) / (self.p * self.grid_size)) * 100