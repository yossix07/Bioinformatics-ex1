import random
import consts


class Person:
    def __init__(self, orginal_belief, location, max_x, max_y):
        self.orginal_belief = orginal_belief
        self.current_belief = orginal_belief
        self.has_rumor = False
        self.rumor_counter = 0
        self.l = 0
        self.location = location
        self.max_x = max_x
        self.max_y = max_y

    def set_belief(self, belief):
        self.orginal_belief = belief
        self.current_belief = belief

    def get_belief(self):
        return self.orginal_belief

    def reset_belief(self):
        self.current_belief = self.orginal_belief
        self.rumor_counter = 0

    def wait_round(self):
        self.l -= 1

    def is_waiting(self):
        if self.l != 0:
            return True
        return False

    def get_neighbors(self, wrap_around):
        x = self.location[0]
        y = self.location[1]
        neighbors = []

        if x < self.max_x - 1:
            neighbors.append([x + 1, y])
        elif wrap_around:
            neighbors.append([0, y])  # add neighbor on opposite side of grid
        if x > 0:
            neighbors.append([x - 1, y])
        elif wrap_around:
            neighbors.append([self.max_x - 1, y])  # add neighbor on opposite side of grid
        if y < self.max_y - 1:
            neighbors.append([x, y + 1])
        elif wrap_around:
            neighbors.append([x, 0])  # add neighbor on opposite side of grid
        if y > 0:
            neighbors.append([x, y - 1])
        elif wrap_around:
            neighbors.append([x, self.max_y - 1])  # add neighbor on opposite side of grid
        if x > 0 and y > 0:
            neighbors.append([x - 1, y - 1])
        elif wrap_around:
            neighbors.append([self.max_x - 1, self.max_y - 1])  # add neighbor on opposite side of grid
        if x < self.max_x - 1 and y > 0:
            neighbors.append([x + 1, y - 1])
        elif wrap_around:
            neighbors.append([0, self.max_y - 1])  # add neighbor on opposite side of grid
        if x > 0 and y < self.max_y - 1:
            neighbors.append([x - 1, y + 1])
        elif wrap_around:
            neighbors.append([self.max_x - 1, 0])  # add neighbor on opposite side of grid
        if x < self.max_x - 1 and y < self.max_y - 1:
            neighbors.append([x + 1, y + 1])
        elif wrap_around:
            neighbors.append([0, 0])  # add neighbor on opposite side of grid
        return neighbors

        # if warp_around:
        #     if x < self.max_x - 1:
        #         neighbors.append([x + 1, y])
        #     if x == self.max_x -1
        #     if x > 0:
        #         neighbors.append([x - 1, y])
        #     if y < self.max_y - 1:
        #         neighbors.append([x, y + 1])
        #     if y > 0:
        #         neighbors.append([x, y - 1])
        #     if x > 0 and y > 0:
        #         neighbors.append([x - 1, y - 1])
        #     if x < self.max_x - 1 and y > 0:
        #         neighbors.append([x + 1, y - 1])
        #     if x > 0 and y < self.max_y - 1:
        #         neighbors.append([x - 1, y + 1])
        #     if x < self.max_x - 1 and y < self.max_y - 1:
        #         neighbors.append([x + 1, y + 1])
        #
        # else:
        #     if x < self.max_x - 1:
        #         neighbors.append([x + 1, y])
        #     if x > 0:
        #         neighbors.append([x - 1, y])
        #     if y < self.max_y - 1:
        #         neighbors.append([x, y + 1])
        #     if y > 0:
        #         neighbors.append([x, y - 1])
        #     if x > 0 and y > 0:
        #         neighbors.append([x - 1, y - 1])
        #     if x < self.max_x - 1 and y > 0:
        #         neighbors.append([x + 1, y - 1])
        #     if x > 0 and y < self.max_y - 1:
        #         neighbors.append([x - 1, y + 1])
        #     if x < self.max_x - 1 and y < self.max_y - 1:
        #         neighbors.append([x + 1, y + 1])

        return neighbors


    def get_neighbors_num(self, matrix,wrap_around):
        counter = 0
        neighbors_locations = self.get_neighbors(wrap_around)

        for neighbor in neighbors_locations:
            x = neighbor[0]
            y = neighbor[1]
            if matrix[x][y] is not None:
                counter += 1
        return counter

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

    def got_rumor(self):
        self.rumor_counter += 1
        if self.rumor_counter > 1:
            self.decrease_rumor()
        if random.random() < consts.belief_dict[self.current_belief]:
            self.set_belive_rumor()
            return True
        return False

    def decrease_rumor(self):
        self.current_belief = self.current_belief - 1 if self.current_belief - 1 >= 1 else 1

    def get_has_rumor(self):
        return self.has_rumor

    def set_belive_rumor(self):
        self.has_rumor = True