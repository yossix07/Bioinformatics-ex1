import numpy as np
from Gui import GridWindow
from grid import Grid
import matplotlib.pyplot as plt

num_runs = 12
generation_runs = 250
L = 2
P = 0.6
S1 = 0.3
S2 = 0.25
S3 = 0.1
S4 = 0.35
mode = "fastSpread"
visual = "belief"
wrap_around = False
run_gui = True

def generate_graph():
    exposed_to_rumor_percentages = []
    has_rumor_percentages = []
    for j in range(num_runs):
        grid = Grid(L, P, S1, S2, S3, S4, wrap_around, mode)
        generation = 0
        exposed_percentages = []
        current_j_has_rumor_percentage = []
        while generation < generation_runs:
            grid.run()
            
            exposed_to_rumor_percentage = grid.exposed_rumor_precentage()
            exposed_percentages.append(exposed_to_rumor_percentage)

            currnet_has_rumor_percentage = grid.has_rumor_precentage()
            current_j_has_rumor_percentage.append(currnet_has_rumor_percentage)

            generation += 1
        has_rumor_percentages.append(current_j_has_rumor_percentage)
        exposed_to_rumor_percentages.append(exposed_percentages)

    avg_exposed_to_rumor_percentages = [np.mean([x[i] for x in exposed_to_rumor_percentages]) for i in range(generation_runs)]
    avg_has_rumor_percentages = [np.mean([x[i] for x in has_rumor_percentages]) for i in range(generation_runs)]

    num_of_generations = [i for i in range(generation_runs)]

    plt.plot(num_of_generations, avg_has_rumor_percentages)
    plt.title(f'parameters: P={P}, L={L},S1={S1},S2={S2}, S3={S3}, S4={S4} ')
    plt.ylabel('Average Believe to Rumor Percentage')
    plt.xlabel('Number of Generations')
    plt.show()


def simulator_gui():
    gui = GridWindow(f'{P}', f'{L}', f'{S1}', f'{S2}', f'{S3}', f'{S4}')
    is_start, l, p, s1, s2, s3, s4 = gui.run_menu()
    if is_start:
        grid = Grid(l, p, s1, s2, s3, s4, wrap_around, mode)
        while gui.running():
            gui.check_if_done()
            grid.run()
            grid.exposed_rumor_precentage()
            gui.draw(grid, visual)

        gui.exit()


if __name__ == "__main__":
    if run_gui:
        simulator_gui()
    else:
        generate_graph()