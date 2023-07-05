import numpy as np
import genetic_functions as genetic
import task_specific_functions as task
import csv
import pandas as pd
import matplotlib.pyplot as plt


def run_experiment():
    # -------------------HIPERPARAMETERS-------------------
    num_experiments = 30
    subject_size = 200
    mi = 30
    pm = 0.11
    iter_max = 1000

    pc_list = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.65, 0.75, 0.8, 0.85]
    pc_list = [0.15, 0.25, 0.35, 0.45, 0.5, 0.6, 0.7, 0.8,  0.55, 0.65, 0.75, 0.85]
 
    objective_function = task.calculate_objective
    reproduction_function = genetic.reproduction_roulette
    mutation_function = genetic.mutation_binary
    crossover_function = genetic.crossover_singlepoint
    succesion_function = genetic.succesion_generational

    # -------------------RUN EXPERIMENTS-------------------
    out_folder = "output_2/"
    for pc in pc_list:

        file_name = "experiment_{}_{}_{}_{}_{}.csv".format(iter_max, num_experiments, mi, pc, pm)
        out_path = out_folder + file_name
        out_file = open(out_folder + file_name, 'w')
        writer = csv.writer(out_file)

        for i in range(0, num_experiments):
            print("-----------------------------", i)
            genotype, gain = genetic.genetic_alghoritm(objective_function, reproduction_function, mutation_function, 
                                                       crossover_function, succesion_function, 
                                                       subject_size, mi, pm, pc, iter_max)
            writer.writerow([i, gain, *genotype])


def analyse_experiments():
        # -------------------HIPERPARAMETERS-------------------
    num_experiments = 30
    subject_size = 200
    mi = 30
    pc = 0.1
    iter_max = 3000
    dir_name = "output/"

    params = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.65, 0.75, 0.8, 0.85]
    # params = [0.1,  0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.65, 0.75, 0.8, 0.85]
    genes = np.linspace(0, 199, 200)
    genes_int = [int(x) for x in genes]
    genes_str = [str(x) for x in genes_int]
    header = ["id", "out"] + genes_str
    
    # -------------------READ DATA-------------------
    data_list = []
    for pm in params:
        file_name = "experiment_{}_{}_{}_{}_{}.csv".format(iter_max, num_experiments, mi, pc, pm)
        path_name = dir_name + file_name
        
        data = read_data_from_file(path_name, header)

        data_list.append(data['out'].to_list())

        print("\n--------------------------------------------------------")
        print("EXPERIMENT. ITER_MAX: {}, PM: {}".format(iter_max, pm))
        print(data["out"].describe()[['mean', 'std']])
        print()

    fig1, ax1 = plt.subplots()
    ax1.set_title('Badanie dla 30 powtórzeń składających się z 3000 iteracji')
    ax1.boxplot(data_list)
    ax1.set_xlabel("Prawdopodobieństwo mutacji")
    ax1.set_ylabel("wyniki funkcji celu")
    # plt.yscale('log')
    ax1.set_xticklabels(params)
    plt.show()



def read_data_from_file(filename, headers):
    data = pd.read_csv(filename)
    data.columns = headers
    return data


if __name__ == "__main__":
    # run_experiment()
    analyse_experiments()