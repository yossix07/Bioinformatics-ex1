import random
import consts

class Person:
    def __init__(self, orginal_belief, location, max_x, max_y):
        """
        Initializes a person object with given properties.

        Parameters:
        orginal_belief (int): The original belief level of the person.
        location (tuple): The coordinates of the person in the matrix.
        max_x (int): The maximum value of x coordinate in the matrix.
        max_y (int): The maximum value of y coordinate in the matrix.
        """
        self.orginal_belief = orginal_belief
        self.current_belief = orginal_belief
        self.has_rumor = False
        self.rumor_counter = 0
        self.l = 0
        self.location = location
        self.max_x = max_x
        self.max_y = max_y

    def set_belief(self, belief):
        """
        Sets the original and current belief level of the person.

        Parameters:
        belief (int): The new belief level.
        """
        self.orginal_belief = belief
        self.current_belief = belief

    def get_belief(self):
        """
        Returns the original belief level of the person.

        Returns:
        int: The original belief level.
        """
        return self.orginal_belief

    def reset_belief(self):
        """
        Resets the current belief level of the person and rumor counter.
        """
        self.current_belief = self.orginal_belief
        self.rumor_counter = 0

    def wait_round(self):
        """
        Decreases the waiting time of the person by 1.
        """
        self.l -= 1

    def is_waiting(self):
        """
        Returns whether the person is waiting or not.

        Returns:
        bool: True if the person is waiting, False otherwise.
        """
        if self.l != 0:
            return True
        return False

    def get_neighbors(self, wrap_around):
        """
        Returns the coordinates of all neighbors of the person.

        Parameters:
        wrap_around (bool): Whether the matrix wraps around or not.

        Returns:
        list of tuples: The coordinates of all neighbors of the person.
        """
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

    def get_neighbors_num(self, matrix, wrap_around):
        """
        Returns the number of neighbors of the person who have a rumor.

        Parameters:
        matrix (list of lists): The matrix representing the network of people.
        wrap_around (bool): Whether the matrix wraps around or not.

        Returns:
        int: The number of neighbors of the person who have a rumor.
        """
        counter = 0
        neighbors_locations = self.get_neighbors(wrap_around)

        for neighbor in neighbors_locations:
            x = neighbor[0]
            y = neighbor[1]
            if matrix[x][y] is not None:
                if matrix[x][y].got_rumor():
                    counter += 1
        return counter


    def spread_rumor(self, matrix, l, wrap_around):
        """
        Spread the rumor to the person's neighbors.

        Parameters:
        matrix (list of lists): The matrix representing the network of people.
        l (int): The number of rounds which a preson need to wait after spreading the rumor.
        wrap_around (bool): Whether the matrix wraps around or not.

        Returns:
        list: The list of neighbors which are exposed to the rumor from the person.
        list: the list of neighbors which belive to the rumor from the person.
        """
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
        """
        The person recives a rumor.

        Returns:
        bool: True if the person now believes the rumor and False otherwise.
        """
        self.rumor_counter += 1
        if self.rumor_counter > 1:
            self.decrease_rumor()
        if random.random() < consts.belief_dict[self.current_belief]:
            self.set_belive_rumor()
            return True
        return False

    def decrease_rumor(self):
        """
        Decreases the person's belief level(with lower boundary of 1)
        """
        self.current_belief = self.current_belief - 1 if self.current_belief - 1 >= 1 else 1

    def get_has_rumor(self):
        """
        The person now believes the rumor.
        """
        return self.has_rumor

    def set_belive_rumor(self):
        """
        The person now believes the rumor.
        """
        self.has_rumor = True