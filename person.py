import random
import consts

class Person:
    # Initializes a person object with given properties.
    def __init__(self, orginal_belief, location, max_x, max_y):
        self.orginal_belief = orginal_belief
        self.current_belief = orginal_belief
        self.has_rumor = False
        self.rumor_counter = 0
        self.l = 0
        self.location = location
        self.max_x = max_x
        self.max_y = max_y

    # Sets the original and current belief level of the person.
    def set_belief(self, belief):
        self.orginal_belief = belief
        self.current_belief = belief

    # Returns the original belief level of the person.
    def get_belief(self):
        return self.orginal_belief
    
    # Resets the current belief level of the person and rumor counter.
    def reset_belief(self):
        self.current_belief = self.orginal_belief
        self.rumor_counter = 0

    # Decreases the waiting time of the person by 1.
    def wait_round(self):
        self.l -= 1

    # Returns whether the person is waiting or not.
    def is_waiting(self):
        if self.l != 0:
            return True
        return False

    # Returns the coordinates of all neighbors of the person.
    def get_neighbors(self, wrap_around):
        x, y = self.location
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x_neighbor = x + i
                y_neighbor = y + j
                if wrap_around:
                    x_neighbor %= self.max_x
                    y_neighbor %= self.max_y
                if 0 <= x_neighbor < self.max_x and 0 <= y_neighbor < self.max_y:
                    neighbors.append((x_neighbor, y_neighbor))

        return neighbors

    # Returns the number of neighbors of the person who have a rumor.
    def get_neighbors_num(self, matrix, wrap_around):
        counter = 0
        neighbors_locations = self.get_neighbors(wrap_around)

        for neighbor in neighbors_locations:
            x = neighbor[0]
            y = neighbor[1]
            if matrix[x][y] is not None:
                if matrix[x][y].got_rumor():
                    counter += 1
        return counter


    # Spread the rumor to the person's neighbors.
    def spread_rumor(self, matrix, l, wrap_around):
        neighbors_with_rumor = []
        exposed_neighbors = set()
        if self.l == 0:
            self.l = l
            for neighbor in self.get_neighbors(wrap_around):
                neighbor_x, neighbor_y = neighbor
                exposed_neighbors.add(matrix[neighbor_x][neighbor_y])
                if matrix[neighbor_x][neighbor_y] != None and matrix[neighbor_x][neighbor_y].got_rumor():
                    neighbors_with_rumor.append(matrix[neighbor_x][neighbor_y])
        return neighbors_with_rumor, exposed_neighbors

    # The person recives a rumor.
    def got_rumor(self):
        self.rumor_counter += 1
        if self.rumor_counter > 1:
            self.decrease_rumor()
        if random.random() < consts.belief_dict[self.current_belief]:
            self.set_belive_rumor()
            return True
        return False

    # Decreases the person's belief level(with lower boundary of 1)
    def decrease_rumor(self):
        self.current_belief = self.current_belief - 1 if self.current_belief - 1 >= 1 else 1

    # The person now believes the rumor.
    def get_has_rumor(self):
        return self.has_rumor

    # The person now believes the rumor.
    def set_belive_rumor(self):
        self.has_rumor = True