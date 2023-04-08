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
L = 3
P = 0.65
S1 = 0.35
S2 = 0.4
S3 = 0.15
S4 = 0.1
def run_with_graph():
    generation_counts = []
    exposed_to_rumor_percentages = []
    min_len=0
    for j in range(num_runs):
        grid = Grid(L, P, S1, S2, S3, S4)
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
        print("generation", generation)
        has_rumor_percentages.append(current_j_has_rumor_percentage)
        exposed_to_rumor_percentages.append(exposed_percentages)
        # generation_counts.append(generation)
        
    # Take the minimum length of all exposed percentage lists across all runs
    # generation_counts.sort()
    # min_len = generation_counts[0]

#    min_len = min([len(x) for x in exposed_to_rumor_percentages])

    # Take the average of each generation across all runs, up to the minimum length
    avg_exposed_to_rumor_percentages = [np.mean([x[i] for x in exposed_to_rumor_percentages]) for i in range(generation_runs)]
    # avg_has_rumor_percentages = [np.mean([x[i] for x in has_rumor_percentages]) for i in range(min_len)]

    # Trim the generation_counts array to match the length of avg_exposed_to_rumor_percentages
    #generation_counts = generation_counts[:min_len]
    #create a list
    # print(min_len)
    num_of_generations = [i for i in range(generation_runs)]

    # Plot the results
    plt.plot(num_of_generations, avg_exposed_to_rumor_percentages)
    plt.title(f'parameters: P={P}, L={L},S1={S1},S2={S2}, S3={S3}, S4={S4} ')
    plt.ylabel('Average Exposed to Rumor Percentage')
    plt.xlabel('Number of Generations')
    plt.show()


def run_with_gui():
    exposed_people = set()
    grid = Grid(L, P, S1, S2, S3, S4)
    window = GridWindow()
    generation = 0
    while window.running():
    #while grid.run():
        window.check_if_done()
        grid.run()
        exposed_to_rumor_percentage = grid.exposed_rumor_precentage()
        #print(exposed_to_rumor_percentage)

        window.draw(grid)
        generation += 1

    window.exit()
    has_rumor_percentage = grid.has_rumor_precentage()


if __name__ == "__main__":
    run_with_graph()