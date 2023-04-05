import consts
import numpy as np
from person import Person


class Grid:
    def __init__(self, l, p, s1_precent, s2_precent, s3_precent, s4_precent):
        self.matrix = [[None for _ in range(consts.Size)] for _ in range(consts.Size)]
        self.l = l
        self.p = p
        self.current_rumor_exposed = set()

        self.same_state_counter = 0
        self.state = None

        s1_number = int(p * s1_precent)
        s2_number = int(p * s2_precent)
        s3_number = int(p * s3_precent)
        s4_number = int(p * s4_precent)
        random_indices = np.random.choice(consts.Size * consts.Size, p, replace=False)
        random_location = np.random.choice(random_indices)
        for idx in random_indices:
            row_idx = idx // consts.Size
            col_idx = idx % consts.Size
            if idx == random_location:
                chosen_location = [row_idx, col_idx]

            person_belief = None
            if s1_number > 0:
                person_belief = 1
                s1_number -= 1
            elif s2_number > 0:
                person_belief = 2
                s2_number -= 1
            elif s3_number > 0:
                person_belief = 3
                s3_number -= 1
            elif s4_number > 0:
                person_belief = 4
                s4_number -= 1
            self.matrix[row_idx][col_idx] = Person(person_belief, [row_idx, col_idx], consts.Size, consts.Size)

        self.matrix[chosen_location[0]][chosen_location[1]].set_belive_rumor()
        self.first_person = self.matrix[chosen_location[0]][chosen_location[1]]
        self.has_rumor_list = {self.first_person}
        self.current_rumor_exposed = {self.first_person}

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
        if self.state is not None and len(self.has_rumor_list) == len(self.state):
            self.same_state_counter += 1
        else:
            self.same_state_counter = 0

        if self.same_state_counter == 5:
            return False

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
        return (len(self.has_rumor_list) / self.p) * 100

    def exposed_rumor_precentage(self):
        return (len(self.current_rumor_exposed) / self.p) * 100