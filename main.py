import numpy as np
from Gui import GridWindow
from grid import Grid
import matplotlib.pyplot as plt
from time import sleep
import consts

run_gui = True

# generate graphs for the report part
def generate_graph():
    exposed_to_rumor_percentages = []
    has_rumor_percentages = []
    for j in range(consts.num_runs):
        grid = Grid(consts.L, consts.P, consts.S1, consts.S2,
                    consts.S3, consts.S4, consts.wrap_around)
        generation = 0
        exposed_percentages = []
        current_j_has_rumor_percentage = []
        while generation < consts.generation_runs:
            grid.run()

            exposed_to_rumor_percentage = grid.exposed_rumor_precentage()
            exposed_percentages.append(exposed_to_rumor_percentage)

            currnet_has_rumor_percentage = grid.has_rumor_precentage()
            current_j_has_rumor_percentage.append(currnet_has_rumor_percentage)

            generation += 1
        has_rumor_percentages.append(current_j_has_rumor_percentage)
        exposed_to_rumor_percentages.append(exposed_percentages)

    avg_exposed_to_rumor_percentages = [np.mean([x[i] for x in exposed_to_rumor_percentages]) for i in
                                        range(consts.generation_runs)]
    avg_has_rumor_percentages = [np.mean([x[i] for x in has_rumor_percentages]) for i in range(consts.generation_runs)]

    num_of_generations = [i for i in range(consts.generation_runs)]

    plt.plot(num_of_generations, avg_exposed_to_rumor_percentages)
    plt.title(f'parameters: P={consts.P}, L={consts.L},S1={consts.S1},S2={consts.S2}, S3={consts.S3}, S4={consts.S4} ')
    plt.ylabel('Average exposed to Rumor Percentage')
    plt.xlabel('Number of Generations')
    plt.show()


# runs the simulation
def simulator_gui():
    gui = GridWindow(f'{consts.P}', f'{consts.L}', f'{consts.S1}', f'{consts.S2}', f'{consts.S3}', f'{consts.S4}')
    is_start, l, p, s1, s2, s3, s4, wrap_around = gui.run_menu()
    if is_start:
        grid = Grid(l, p, s1, s2, s3, s4, wrap_around, consts.modeFast)
        while gui.running():
            gui.check_if_done()
            grid.run()
            grid.exposed_rumor_precentage()
            gui.draw(grid, consts.visual)

        gui.exit()
    else:
        sleep(3)


if __name__ == "__main__":
    if run_gui:
        simulator_gui()
    else:
        generate_graph()