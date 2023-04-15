import csv
import numpy as np
from Gui import GridWindow
from grid import Grid
import matplotlib.pyplot as plt

l_array = [1, 3, 5, 10, 15]
p_array = [5000, 6000, 7000, 8000, 9000]
s1_array = [0.1, 0.2, 0.3, 0.4, 0, 0.25]
s2_array = [0.2, 0.3, 0.4, 0.1, 0.1, 0.25]
s3_array = [0.3, 0.4, 0.1, 0.2, 0.5, 0.25]
s4_array = [0.4, 0.1, 0.2, 0.3, 0.4, 0.25]

num_runs = 12
generation_runs = 250
L = 2
P = 0.6
S1 = 0.3
S2 = 0.25
S3 = 0.1
S4 = 0.35
mode = "slowSpread"
visual = "has_rumor"
wrap_around=True


def run_with_graph():
    generation_counts = []
    exposed_to_rumor_percentages = []
    min_len = 0
    for j in range(num_runs):
        grid = Grid(L, P, S1, S2, S3, S4,wrap_around)
        exposed_people = set()
        generation = 0
        exposed_percentages = []
        has_rumor_percentages = []
        current_j_has_rumor_percentage = []
        while generation < generation_runs:
            grid.run()
            exposed_to_rumor_percentage = grid.exposed_rumor_precentage()
            exposed_percentages.append(exposed_to_rumor_percentage)
            generation += 1
            currnet_has_rumor_percentage = grid.has_rumor_precentage()
            current_j_has_rumor_percentage.append(currnet_has_rumor_percentage)
        print(exposed_to_rumor_percentage)
        has_rumor_percentages.append(current_j_has_rumor_percentage)
        exposed_to_rumor_percentages.append(exposed_percentages)
        # generation_counts.append(generation)

    # Take the average of each generation across all runs, up to the minimum length
    avg_exposed_to_rumor_percentages = [np.mean([x[i] for x in exposed_to_rumor_percentages]) for i in range(generation_runs)]
    #avg_has_rumor_percentages = [np.mean([x[i] for x in has_rumor_percentages]) for i in range(generation_runs)]

    # create a list
    num_of_generations = [i for i in range(generation_runs)]

    # Plot the results
    plt.plot(num_of_generations, avg_exposed_to_rumor_percentages)
    plt.title(f'parameters: P={P}, L={L},S1={S1},S2={S2}, S3={S3}, S4={S4} ')
    plt.ylabel('Average Exposed to Rumor Percentage')
    plt.xlabel('Number of Generations')
    plt.show()


def run_with_gui():
    exposed_people = set()
    gui = GridWindow(f'{P}', f'{L}', f'{S1}', f'{S2}', f'{S3}', f'{S4}')
    is_start, l, p, s1, s2, s3, s4 = gui.run_menu()
    if is_start:
        grid = Grid(l, p, s1, s2, s3, s4, mode)
        generation = 0
        while gui.running():
            # while grid.run():
            gui.check_if_done()
            grid.run()
            exposed_to_rumor_percentage = grid.exposed_rumor_precentage()
            # print(exposed_to_rumor_percentage)

            gui.draw(grid, visual)
            generation += 1

        gui.exit()
        has_rumor_percentage = grid.has_rumor_precentage()


if __name__ == "__main__":
    #run_with_gui()
    run_with_graph()