import consts
import numpy as np
from person import Person
from collections import deque

class Grid:
    def __init__(self, l, p, s1_precent, s2_precent, s3_precent, s4_precent, mode='random'):
        self.matrix = [[None for _ in range(consts.Size)] for _ in range(consts.Size)]
        self.l = l
        self.p = p
        self.current_rumor_exposed = set()
        self.grid_size = consts.Size * consts.Size
        self.same_state_counter = 0
        self.state = None

        s1_number = int(p * self.grid_size * s1_precent)
        s2_number = int(p * self.grid_size * s2_precent)
        s3_number = int(p * self.grid_size * s3_precent)
        s4_number = int(p * self.grid_size * s4_precent)

        print(s1_number, s2_number, s3_number, s4_number)
        
        if mode == 'random':
            chosen_location = self.init_at_random_locations(s1_number, s2_number, s3_number, s4_number)
        if mode == 'slowSpread':
            chosen_location = self.init_slow_spread_diagonal(s1_number, s2_number, s3_number, s4_number)

        self.matrix[chosen_location[0]][chosen_location[1]].set_belive_rumor()
        self.first_person = self.matrix[chosen_location[0]][chosen_location[1]]
        self.has_rumor_list = {self.first_person}
        self.current_rumor_exposed = {self.first_person}

    def init_at_random_locations(self, s1_number, s2_number, s3_number, s4_number):
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]

            s_numbers = [s1_number, s2_number, s3_number, s4_number]
            person_belief = 3
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
            
            self.matrix[row_idx][col_idx] = Person(2, [row_idx, col_idx], consts.Size, consts.Size)

        round = deque([1, 2, 3, 4])
        belief_counts = {1: s1_number, 2: s2_number, 3: s3_number, 4: s4_number}

        for row in range(consts.Size):
            for col in range(consts.Size):
                if self.matrix[row][col] is not None:
                    belief_num = round[0]
                    self.matrix[row][col].set_belief(belief_num)
                    print(row, col, belief_num)
                    if belief_num in belief_counts:
                        belief_counts[belief_num] -= 1
                        if belief_counts[belief_num] == 0:
                            round.popleft()
                        if len(round) == 0:
                            break
                    round.rotate(-1)
        return chosen_location        
    
    
    def init_slow_spread_diagonal(self, s1_number, s2_number, s3_number, s4_number):
        random_indices = np.random.choice(consts.Size * consts.Size, int(self.p * self.grid_size), replace=False)
        random_location = np.random.choice(random_indices)        
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]
            
            self.matrix[row_idx][col_idx] = Person(2, [row_idx, col_idx], consts.Size, consts.Size)

        round = deque([1, 2, 3, 4])

        is_break = False
        for i in range(consts.Size):
            diagonal = [self.matrix[j][j+i] for j in range(consts.Size-i) if self.matrix[j][j+i] is not None]
            diagonal1 = [self.matrix[j+i][j] for j in range(consts.Size-i) if self.matrix[j+i][j] is not None]
            for person in diagonal:
                person.set_belief(round[0])
                # print(person.location[0], person.location[1], round[0])
                if round[0] == 1:
                    s1_number -= 1
                    if s1_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                if round[0] == 2:
                    s2_number -= 1
                    if s2_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                if round[0] == 3:
                    s3_number -= 1
                    if s3_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                if round[0] == 4:
                    s4_number -= 1
                    if s4_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                round.rotate(-1)
            if is_break:
                break
            for person in diagonal1:
                person.set_belief(round[0])
                # print(person.location[0], person.location[1], round[0])
                if round[0] == 1:
                    s1_number -= 1
                    if s1_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                if round[0] == 2:
                    s2_number -= 1
                    if s2_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                if round[0] == 3:
                    s3_number -= 1
                    if s3_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                if round[0] == 4:
                    s4_number -= 1
                    if s4_number == 0:
                        round.popleft()
                if len(round) == 0:
                    is_break = True
                    break
                round.rotate(-1)
            if is_break:
                break
            

        # print(round)
        # is_break = False
        # for i in range(1, consts.Size):
        #     if is_break:
        #         break
        #     diagonal = [self.matrix[j+i][j] for j in range(consts.Size-i) if self.matrix[j+i][j] is not None]
        #     for person in diagonal:
        #         person.set_belief(round[0])
        #         # print(person.location[0], person.location[1], round[0])
        #         if round[0] == 1:
        #             s1_number -= 1
        #             if s1_number == 0:
        #                 round.popleft()
        #         if len(round) == 0:
        #             is_break = True
        #             break
        #         if round[0] == 2:
        #             s2_number -= 1
        #             if s2_number == 0:
        #                 round.popleft()
        #         if len(round) == 0:
        #             is_break = True
        #             break
        #         if round[0] == 3:
        #             s3_number -= 1
        #             if s3_number == 0:
        #                 round.popleft()
        #         if len(round) == 0:
        #             is_break = True
        #             break
        #         if round[0] == 4:
        #             s4_number -= 1
        #             if s4_number == 0:
        #                 round.popleft()
        #         if len(round) == 0:
        #             is_break = True
        #             break
        #         round.rotate(-1)
        return chosen_location


    def run(self):
        current_round_rumor_set = set()

        for person in self.has_rumor_list:
            believers_to_rumor, exposed_to_rumor = person.spread_rumor(self.matrix, self.l)
            current_round_rumor_set.update(believers_to_rumor)
            self.current_rumor_exposed = self.current_rumor_exposed.union(exposed_to_rumor)

        self.state = self.has_rumor_list
        #self.current_rumor_exposed = self.current_rumor_exposed.union(exposed_to_rumor)
        #print(f'exposed: {len(self.current_rumor_exposed)}')
        self.has_rumor_list = self.has_rumor_list.union(current_round_rumor_set)
        # if self.state is not None and len(self.has_rumor_list) == len(self.state):
        #     self.same_state_counter += 1
        # else:
        #     self.same_state_counter = 0

        # if self.same_state_counter == 100:
        #     return False

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