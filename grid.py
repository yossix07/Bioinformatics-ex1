import consts
import numpy as np
from person import Person

class Grid:
    def __init__(self, l, p, s1_precent, s2_precent, s3_precent, s4_precent, mode='random'):
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
        
        if mode == 'random':
            chosen_location = self.init_at_random_locations(s1_number, s2_number, s3_number, s4_number)
        if mode == 'slowSpread':
            chosen_location = self.init_slow_spread(s1_number, s2_number, s3_number, s4_number)

        self.matrix[chosen_location[0]][chosen_location[1]].set_belive_rumor()
        self.first_person = self.matrix[chosen_location[0]][chosen_location[1]]
        self.has_rumor_list = {self.first_person}
        self.current_rumor_exposed = {self.first_person}

    def init_at_random_locations(self, s1_number, s2_number, s3_number, s4_number):
        random_indices = np.random.choice(consts.Size * consts.Size, self.p, replace=False)
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
        return chosen_location

    def init_slow_spread(self, s1_number, s2_number, s3_number, s4_number):
        high_belief_clusters = []
        low_belief_locations = []

        # Create high belief clusters
        for s_number, belief in [(s1_number, 1), (s2_number, 2), (s3_number, 3), (s4_number, 4)]:
            for i in range(s_number):
                # Choose random location within the grid
                location = [np.random.randint(consts.Size), np.random.randint(consts.Size)]
                # Create person object with high belief
                person = Person(belief, location, consts.Size, consts.Size)
                # Append person to high belief cluster
                high_belief_clusters.append(person)

        # Place high belief clusters in different parts of the grid
        for i, cluster in enumerate(high_belief_clusters):
            # Compute size of the cluster
            cluster_size = len(high_belief_clusters) // 4
            if i == 0:
                # Place first cluster in random location
                row_idx, col_idx = cluster.location
            elif i == 1:
                # Place second cluster in opposite corner
                row_idx = consts.Size - cluster_size
                col_idx = consts.Size - cluster_size
            elif i == 2:
                # Place third cluster in random row, first or last column
                row_idx = np.random.randint(consts.Size - cluster_size)
                col_idx = np.random.choice([0, consts.Size - cluster_size])
            else:
                # Place fourth cluster in first or last row, random column
                row_idx = np.random.choice([0, consts.Size - cluster_size])
                col_idx = np.random.randint(consts.Size - cluster_size)

            # Update location of all persons in the cluster
            for j in range(cluster_size):
                for k in range(cluster_size):
                    location = [row_idx + j, col_idx + k]
                    if location == cluster.location:
                        # Update location of first person
                        cluster.location = location
                    else:
                        # Create person object with low belief and append to low_belief_locations list
                        person = Person(0, location, consts.Size, consts.Size)
                        low_belief_locations.append(person)

            # Update location of the high belief cluster
            cluster.location = [row_idx + cluster_size // 2, col_idx + cluster_size // 2]
            self.matrix[cluster.location[0]][cluster.location[1]] = cluster

        # Place people with low belief around high belief clusters
        for person in low_belief_locations:
            row_idx, col_idx = person.location
            if self.matrix[row_idx][col_idx] is None:
                # Check if location is empty
                # Find distance to closest high belief person
                min_distance = consts.Size * 2
                for cluster in high_belief_clusters:
                    distance = np.sqrt((row_idx - cluster.location[0]) ** 2 + (col_idx - cluster.location[1]) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                if min_distance <= self.l:
                    # Place person if within range of a high belief person
                    self.matrix[row_idx][col_idx] = person
        random_high_belief_person = np.random.choice(high_belief_clusters)
        random_low_belief_person = np.random.choice(low_belief_locations)
        chosen_person = np.random.choice([random_high_belief_person, random_low_belief_person])
        return chosen_person.location


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